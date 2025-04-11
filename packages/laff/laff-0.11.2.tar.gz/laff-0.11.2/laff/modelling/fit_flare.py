import numpy as np
import logging
import emcee
from intersect import intersection
from ..utility import calculate_fit_statistics
from ..modelling import broken_powerlaw

logger = logging.getLogger('laff')

#################################################################################
### FRED MODEL
#################################################################################

def fred_flare(x, params):
    # J. P. Norris et al., ‘Attributes of Pulses in Long Bright Gamma-Ray Bursts’, The Astrophysical Journal, vol. 459, p. 393, Mar. 1996, doi: 10.1086/176902.
    
    x = np.array(x)
    t_max = params[0]
    rise = params[1]
    decay = params[2]
    sharpness = params[3]
    amplitude = params[4]

    model = amplitude * np.exp( -(abs(x - t_max) / rise) ** sharpness)
    model[np.where(x > t_max)] = amplitude * np.exp( -(abs(x[np.where(x > t_max)] - t_max) / decay) ** sharpness)

    return model

def fred_flare_wrapper(params, x):
    return fred_flare(x, params)

def all_flares_fred(x, params):
    x = np.array(x)

    flare_params = [params[i:i+4] for i in range(0, len(params), 4)]
    
    sum_all_flares = [0.0] * len(x)

    for flare in flare_params:
        fit_flare = fred_flare(x, flare)
        sum_all_flares = [prev + current for prev, current in zip(sum_all_flares, fit_flare)]

    return sum_all_flares



def old_fred_flare(x, params):
    x = np.array(x)
    tau = params[0]
    rise = params[1]
    decay = params[2]
    amplitude = params[3]

    cond = x < tau  

    model = amplitude * np.sqrt(np.exp(2*(rise/decay))) * np.exp(-(rise/(x-tau))-((x-tau)/decay))
    model[np.where(cond)] = 0

    return model

def old_fred_flare_wrapper(params, x):
    return old_fred_flare(x, params)

def old_all_flares_fred(x, params):
    x = np.array(x)

    flare_params = [params[i:i+4] for i in range(0, len(params), 4)]
    
    sum_all_flares = [0.0] * len(x)

    for flare in flare_params:
        fit_flare = old_fred_flare(x, flare)
        sum_all_flares = [prev + current for prev, current in zip(sum_all_flares, fit_flare)]

    return sum_all_flares

#################################################################################
### GAUSSIAN MODEL
#################################################################################

def gaussian_flare(x, params):
    x = np.array(x)
    centre = params[0]
    height = params[1]
    width = np.abs(params[2])

    model = height * np.exp(-((x-centre)**2)/(2*(width**2)))

    return model

def gaussian_flare_wrapper(params, x):
    return gaussian_flare(x, params)

def all_flare_gauss(x, params):
    x = np.array(x)

    flare_params = [params[i:i+3] for i in range(0, len(params), 3)]
    
    sum_all_flares = [0.0] * len(x)

    for flare in flare_params:
        fit_flare = gaussian_flare(x, flare)
        sum_all_flares = [prev + current for prev, current in zip(sum_all_flares, fit_flare)]

    return sum_all_flares

#################################################################################
### SCIPY.ODR FITTING
#################################################################################

from scipy.odr import ODR, Model, RealData

def flare_fitter(data, continuum, flares, model='fred', skip_mcmc=False):
    """ 
    Flare fitting function. Takes already found flare indices and models them.

    Also runs:
      - 
    
    """
    logger.info("Fitting flares...")

    logger.debug("Calculating residuals")   

    fitted_model = broken_powerlaw(continuum['parameters'], data.time)
    residuals = data.copy()
    residuals['flux'] = data.flux - fitted_model

    flareFits = []
    flareErrs = []

    for start, peak, end in flares:

        data_flare = data.copy()
        data_flare['flux'] = np.float64(0)
        data_flare.loc[start:end, 'flux'] = residuals.loc[start:end, 'flux']

        if model == 'fred':
            flare_model = fred_flare
            model_wrapper = fred_flare_wrapper

            # Parameter estimates.
            t_max = residuals['time'].iloc[peak]
            rise = t_max - residuals['time'].iloc[start]
            decay = residuals['time'].iloc[end] - t_max
            sharpness = decay/rise
            amplitude = residuals['flux'].iloc[peak]
            input_par = [t_max, rise, decay, sharpness, amplitude]

        elif model == 'gauss':
            flare_model = gaussian_flare
            model_wrapper = gaussian_flare_wrapper

            # Parameter estimate.
            centre = residuals['time'].iloc[peak]
            height = residuals['flux'].iloc[peak]
            width = residuals['time'].iloc[peak] - residuals['time'].iloc[start]
            input_par = [centre, height, width]

        # Perform intial ODR fit.
        logger.debug(f"For flare indices {start}/{peak}/{end}:")
        odr_par, odr_err = odr_fitter(data_flare, input_par, model_wrapper)
        # odr_par = [abs(x) for x in odr_par]
        odr_stats = calculate_fit_statistics(data, flare_model, odr_par, temp_flare_shell=True)
        odr_rchisq = odr_stats['rchisq']
        logger.debug(f"ODR Par: {odr_par}")
        logger.debug(f"ODR Err: {odr_err}")

        if skip_mcmc == True:
            # Attempt mcmc fitting routine.
            try:
                mcmc_par, mcmc_err = fit_flare_mcmc(data_flare, input_par, odr_err)
                mcmc_stats = calculate_fit_statistics(data, flare_model, mcmc_par)
                mcmc_rchisq = mcmc_stats['rchisq']
                logger.debug(f"MCMC Par: {mcmc_par}")
                logger.debug(f"MCMC Err: {mcmc_err}")

                # Check for bad MCMC.
                if mcmc_rchisq == 0 or mcmc_rchisq < 0.1 or mcmc_rchisq == np.inf or mcmc_rchisq == -np.inf:
                    logger.debug(f'MCMC appears to be bad, using ODR fit for flare {start}-{end}.')
                    final_par, final_err, final_fit_statistics = odr_par, odr_err, odr_stats
                # Compare the two models.
                elif abs(odr_rchisq-1) < abs(mcmc_rchisq-1):
                    if abs(odr_rchisq) < 1.3 * abs(mcmc_rchisq-1):
                        logger.debug(f"ODR better than MCMC for flare {start}-{end}, using ODR.")
                        final_par, final_err, final_fit_statistics = odr_par, odr_err, odr_stats
                    else:
                        logger.debug(f"ODR better than MCMC fit for flare {start}-{end}, but not significantly enough.")
                # Otherwise: mcmc.
                else:
                    logger.debug("Using MCMC fit.")
                    final_par, final_err, final_fit_statistics = mcmc_par, mcmc_err, mcmc_stats
            except IndexError:
                logger.debug(f"Using ODR fit - likely gaussian curve. Not implemented in MCMC yet.")
                final_par, final_err = odr_par, odr_err
            except ValueError:
                logger.debug(f'MCMC failed - using ODR fit.')
                final_par, final_err = odr_par, odr_err
        else:
            final_par, final_err = odr_par, odr_err


        # Remove from residuals.
        fitted_flare = flare_model(data.time, final_par)
        residuals['flux'] -= fitted_flare
        
        # import matplotlib.pyplot as plt
        # import pandas as pd

        # print(residuals[['time', 'flux']])
        # plt.scatter(residuals.time, residuals.flux)
        # plt.plot(residuals.time, fitted_flare)
        # plt.semilogx()
        # plt.show()

        logger.debug("Flare complete")

        flareFits.append(list(final_par))
        flareErrs.append(list(final_err))

    logger.info("Flare fitting complete for all flares.")
    return flareFits, flareErrs


def improved_end_time(data, flare_indices, flare_par, continuum_par):
    """
    Find the end of the flares based on flare converging to continuum.
    
    Calculate the value of the fitted continuum model to the flare+continuum
    model for a series of values until the models converge. Since the FRED
    model is asymptotic to 0, we apply 'factor' to the flare+continuum, an
    small effective downshift.
    
    Parameters:
    data (pd.DataFrame): GRB lightcurve data.
    flare_indices (List[int]): a nested list of indices corresponding to flare
                               start, stop and end times.
    flare_par (List[float]): a list of the flare model parameters.
    continuum_par (List[floart]): a list of the continuum model parameters.

    Returns:
    end_index (int): the newly found index for the end of the flare.
    end_time (float): the newly found time for the end of the flare.
    """

    logger.debug(f"Running improved_end_time for flare: {flare_indices}.")
    peak, end = flare_indices[1:]
    factor = 0.99 # seems to be the most consistent value.

    if end == len(data.time) - 1:
        logger.debug("End of flare already at end of data. Returning original inputs.")
        return end, data['time'].iloc[end]

    # Calculate value for each model at current flare end.
    current_continuum = broken_powerlaw([data['time'].iloc[end]], continuum_par)[0]
    current_flare = fred_flare([data['time'].iloc[end]], flare_par)[0]
    current_flare += (current_continuum * factor)

    # Loop until the flare+continuum model drops below the continuum.
    extend = 0
    while current_flare > current_continuum and end + extend < len(data.time) -1:
        extend += 1
        logger.debug(f"Conditions not yet met -- extending to {extend}")
        current_continuum = broken_powerlaw([data['time'].iloc[end+extend]], continuum_par)[0]
        current_flare = fred_flare([data['time'].iloc[end+extend]], flare_par)[0]
        current_flare += (current_continuum * factor)
    end_index = end + extend
    logger.debug(f"Conditions met! Calculating intercept.")
        
    # Calculate the intercept time.
    search_time = np.logspace(
        np.log10(data['time'].iloc[peak+1]), 
        np.log10(data['time'].iloc[end+extend+1]),
        num = 1000)
    
    continuum_model = broken_powerlaw(search_time, continuum_par)
    flare_model = fred_flare(search_time, flare_par) + (continuum_model * factor)
    end_time, _ = intersection(search_time, continuum_model, search_time, flare_model)

    # If no intersect found:
    if len(end_time) == 0:
        # print("NO TIME FOUND")
        end_time = data['time'].iloc[end]

    elif len(end_time) > 1:
        logger.warning("Multiple intercepts found for this burst - the flare \
                       may be incorrect or modelled badly.")
        end_time = end_time[-1]
        # print("WEVE ENTERED GREATER THAN ONE")
        # import matplotlib.pyplot as plt
        # plt.plot(search_time, continuum_model, color='tab:orange')
        # plt.plot(search_time, flare_model, color='r')
        # plt.scatter(data.time, data.flux, color='b', marker='.')
        # plt.loglog()
        # plt.show()
        # raise ValueError("It appears two intercepts were found!")
        ## This can occur when the found flare isn't really a flare. Noisy data
        ## etc will cause the flare to be modelled wrong, and so multiple
        ## intersections happen. I can't think of a scenario otherwise? There
        ## should only ever be 2, so just select the later one in this case.
        ## Maybe I can remove this check with better flare finding?
    else:
        end_time = end_time[0]
        # print("WEVE NOT NOT NOT")
    logger.debug(f"Found new end information: index {end_index}, end_time {end_time}.")
    # print(end_time)
    return end_index, end_time


#################################################################################
### FITTING METHODS
#################################################################################

def odr_fitter(data, inputpar, model_wrapper):
    data = RealData(data.time, data.flux, data.time_perr, data.flux_perr)  
    model = Model(model_wrapper)
    odr = ODR(data, model, beta0=inputpar)

    odr.set_job(fit_type=0)
    output = odr.run()

    if output.info != 1:
        i = 1
        while output.info != 1 and i < 100:
            output = odr.restart()
            i += 1

    return output.beta, output.sd_beta

def fit_flare_mcmc(data, init_param, init_err):

    ndim = len(init_param)
    nwalkers = 30
    nsteps = 300

    p0 = np.zeros((nwalkers, ndim))

    guess_tstart = init_param[0]
    std_tstart = init_param[0]
    p0[:, 0] = guess_tstart + std_tstart * np.random.randn(nwalkers)

    guess_rise = init_param[1]
    std_rise = init_param[1]
    p0[:, 1] = guess_rise + std_rise * np.random.randn(nwalkers)

    guess_decay = init_param[2]
    std_decay = init_param[2]
    p0[:, 2] = guess_decay + std_decay * np.random.randn(nwalkers)

    guess_amplitude = init_param[3]
    std_ampltiude = init_param[3]
    p0[:, 3] = guess_amplitude + std_ampltiude * np.random.randn(nwalkers)

    logger.debug("Running flare MCMC...")

    sampler = emcee.EnsembleSampler(nwalkers, ndim, fl_log_posterior, \
        args=(data.time, data.flux, data.time_perr, data.flux_perr))
    sampler.run_mcmc(p0, nsteps)

    burnin = 50

    samples = sampler.chain[:, burnin:, :].reshape(-1, ndim)

    fitted_par = list(map(lambda v: np.median(v), samples.T))
    fitted_err = list(map(lambda v: np.std(v), samples.T))

    logger.debug("MCMC run completed.")

    return fitted_par, fitted_err

def fl_log_likelihood(params, x, y, x_err, y_err):
    model = fred_flare(x, params)
    chisq = np.sum(( (y-model)**2) / ((y_err)**2)) 
    log_likelihood = -0.5 * np.sum(chisq + np.log(2 * np.pi * y_err**2))
    return log_likelihood   

def fl_log_prior(params, TIME_END):

    tau = params[0]
    rise = params[1]
    decay = params[2]
    amplitude = params[3]

    if not (tau > 0) and (tau < TIME_END):
        return -np.inf

    if rise < 0:
        return -np.inf
    if rise > TIME_END:
        return -np.inf

    if decay < 0:
        return -np.inf
    if decay > TIME_END:
        return -np.inf

    if amplitude < 0:
        return -np.inf

    return 0.0

def fl_log_posterior(params, x, y, x_err, y_err):
    lp = fl_log_prior(params, x.iloc[-1])
    ll = fl_log_likelihood(params, x, y, x_err, y_err)
    if not np.isfinite(lp):
        return -np.inf
    return lp + ll