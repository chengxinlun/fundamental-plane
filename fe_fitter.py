import os
import numpy as np
import pickle
import matplotlib.pylab as plt
from astropy.modeling import models, fitting
import warnings
import fe_temp_observed
from base import read_raw_data, get_total_rmid_list, mask_points, check_line, extract_fit_part, save_fig
from position import Location
import time
from multiprocessing import Pool, Manager
from functools import partial

# Define a special class for raising any exception related during the fit


class SpectraException(Exception):
    pass


# Function to fit quasar with the template
def template_fit(wave, flux, error, rmid, mjd):
    img_directory = Location.project_loca + "result/fit_with_temp/fig/" + str(rmid)
    # Fit continuum
    fig = plt.figure()
    plt.plot(wave, flux)
    [cont_wave, cont_flux, cont_error] = extract_fit_part(wave, flux, error, 4040, 4060)
    [temp_wave, temp_flux, temp_error] = extract_fit_part(wave, flux, error, 5080, 5100)
    cont_wave = np.append(cont_wave, temp_wave)
    cont_flux = np.append(cont_flux, temp_flux)
    cont_error = np.append(cont_error, temp_error)
    cont_fitter = fitting.LevMarLSQFitter()
    try:
        cont = models.PowerLaw1D(cont_flux[0], cont_wave[0], - np.log(cont_flux[-1]/cont_flux[0]) / np.log(cont_wave[-1]/cont_wave[0]), fixed = {"x_0": True})
    except Exception as reason:
        save_fig(fig, img_directory, str(mjd) + "-cont-notfound")
        plt.close()
        raise SpectraException("Continuum not found because of " + str(reason))
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            cont_fit = cont_fitter(cont, cont_wave, cont_flux, weights = cont_error ** (-2), maxiter = 10000)
        except Exception as reason:
            save_fig(fig, img_directory, str(mjd) + "-cont-failed")
            plt.close()
            raise SpectraException("Continuum fit failed because of " + str(reason))
    plt.plot(wave, cont_fit(wave))
    save_fig(fig, img_directory, str(mjd) + "-cont-success")
    plt.close()
    # Fit emission lines
    flux = flux - cont_fit(wave)
    fig1 = plt.figure()
    plt.plot(wave, flux)
    hbeta_complex_fit_func = \
            fe_temp_observed.FeII_template_obs(0.0, 2000.0, 2.6, 0.0, 2000.0, 2.6) + \
            models.Gaussian1D(3.6, 4853.30, 7.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4830, 4880], "stddev": [0.0, 10.1]}) + \
            models.Gaussian1D(3.6, 4853.30, 40.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4830, 4880], "stddev": [10.1, 500.0]}) + \
            models.Gaussian1D(2.0, 4346.40, 2.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4323, 4369], "stddev": [0.0, 50.0]}) + \
            models.Gaussian1D(2.0, 4101.73, 2.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4078, 4125], "stddev": [0.0, 50.0]}) + \
            models.Gaussian1D(5.0, 4960.0, 6.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4937, 4983], "stddev": [0.0, 23.8]}) + \
            models.Gaussian1D(20.0, 5008.0, 6.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4985, 5031], "stddev": [0.0, 23.8]})
    fitter = fitting.LevMarLSQFitter()
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            fit = fitter(hbeta_complex_fit_func, wave, flux, weights = error ** (-2), maxiter = 3000)
        except Exception as reason:
            save_fig(fig1, img_directory, str(mjd) + "-failed")
            plt.close()
            raise SpectraException("Fit failed because of " + str(reason))
    #if fit.parameters[2] < 0.0 or fit.parameters[5] < 0.0:
    #    save_fig(fig1, img_directory, str(mjd) + "-failed")
    #    plt.close()
    #    raise SpectraException("Fit failed because of intensity of FeII < 0")
    expected = np.array(fit(wave))
    plt.plot(wave, expected)
    save_fig(fig1, img_directory, str(mjd) + "-succeed")
    plt.close()
    rcs = 0
    for i in range(len(flux)):
        rcs = rcs + (flux[i] - expected[i]) ** 2.0
    rcs = rcs / np.abs(len(flux)-17)
    if rcs > 10.0:
        raise SpectraException("Reduced chi-square too large: " + str(rcs))
    return fit.parameters, cont_fit.parameters, rcs


# Function to output fit result
def output_fit(fit_result, rmid, mjd, band):
    picklefile = open(Location.project_loca + "result/fit_with_temp/data/" + str(rmid) + "/" + str(mjd) + "-" + band + ".pkl", "wb")
    pickle.dump(fit_result, picklefile)
    picklefile.close()


# Exception logging process
def exception_logging(rmid, mjd, reason):
    log = open(Location.project_loca + "Fe2_fit_error.log", "a")
    log.write(str(rmid) + " " + str(mjd) + " " + str(reason) + "\n")
    log.close()


# Individual working process
def fe_fitter_single(rmid, lock, mjd):
    # Read data and preprocessing
    [wave, flux, error] = read_raw_data(rmid, mjd)
    [wave, flux, error] = mask_points(wave, flux,  error)
    [wave, flux, error] = extract_fit_part(wave, flux, error, 4000.0, 5500.0)
    os.chdir(Location.project_loca + "result/fit_with_temp/data")
    try:
        os.mkdir(str(rmid))
    except OSError:
        pass
    os.chdir(Location.project_loca + "result/fit_with_temp/fig")
    try:
        os.mkdir(str(rmid))
    except OSError:
        pass
    # Begin fitting and handling exception
    try:
        [fit_res, cont_res, rcs] = template_fit(wave, flux, error, rmid, mjd)
    except SpectraException as reason:
        lock.acquire()
        exception_logging(rmid, mjd, reason)
        print("Failed for " + str(rmid))
        lock.release()
        return
    output_fit(fit_res, rmid, mjd, "Fe2")
    output_fit(cont_res, rmid, mjd, "cont")
    lock.acquire()
    print("Finished for " + str(mjd))
    lock.release()


def fe_fitter(rmid):
    print("Beginning process for " + str(rmid))
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" + str(rmid)))
    pool = Pool(processes = 4)
    m = Manager()
    lock = m.Lock()
    f = partial(fe_fitter_single, rmid, lock)
    pool.map(f, mjd_list)
    pool.close()
    pool.join()
    print("Finished\n\n")
