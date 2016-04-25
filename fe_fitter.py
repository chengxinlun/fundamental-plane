import os
import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')  # Disable X11
import matplotlib.pylab as plt
from astropy.modeling import models, fitting
import warnings
import fe_temp_observed
from base import read_raw_data, mask_points, extract_fit_part, save_fig
from position import Location
from multiprocessing import Pool, Manager
from functools import partial

# Define a special class for raising any exception related during the fit


class SpectraException(Exception):
    pass


# Function to fit quasar with the template
def template_fit(wave, flux, error, image_control, init_value, rmid, mjd):
    img_directory = Location.project_loca + "result/fit_with_temp/fig/" + \
        str(rmid)
    # Fit continuum
    if image_control:  # Control image output
        fig = plt.figure()
        plt.plot(wave, flux)
    cont_fitter = fitting.LevMarLSQFitter()
    if init_value == []:
        cont = fe_temp_observed.FeII_template_obs(0.0, 2000.0, 2.6, 0.0, 2000.0, 2.6) + \
            models.PowerLaw1D(flux[0], wave[0], - np.log(flux[-1]/flux[0]) / np.log(wave[-1]/wave[0]), fixed = {"x_0": True})
    else:
        fe2_param = init_value[1][0:6]
        cont = fe_temp_observed.FeII_template_obs(fe2_param[0], fe2_param[1],
                                                  fe2_param[2], fe2_param[3],
                                                  fe2_param[4], fe2_param[5]) + \
            models.PowerLaw1D(init_value[0][0], init_value[0][1], init_value[0][2], fixed = {"x_0": True})
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            cont_fit = cont_fitter(cont, wave, flux, weights = error ** (-2), maxiter = 10000)
        except Exception as reason:
            if image_control:  # Control image output
                save_fig(fig, img_directory, str(mjd) + "-cont-failed")
                plt.close()
            raise SpectraException("Continuum fit failed because of " +
                                   str(reason))
    if image_control:  # Control image output
        para = cont_fit.parameters[6:9]
        cont_cont = models.PowerLaw1D(para[0], para[1], para[2])
        cont_spec = cont_cont(wave)
        fit_spec = cont_fit(wave)
        plt.plot(wave, fit_spec)
        plt.plot(wave, cont_spec)
        plt.plot(wave, fit_spec - cont_spec)
        save_fig(fig, img_directory, str(mjd) + "-cont-success")
        plt.close()
    # Fit emission lines
    flux = flux - cont_fit(wave)
    if image_control:  # Control image output
        fig1 = plt.figure()
        plt.plot(wave, flux)
    if init_value == []:
        hbeta_complex_fit_func = \
            models.Gaussian1D(3.6, 4853.30, 7.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4830, 4880], "stddev": [0.0001, 10.1]}) + \
            models.Gaussian1D(3.6, 4853.30, 40.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4830, 4880], "stddev": [10.1, 500.0]}) + \
            models.Gaussian1D(2.0, 4346.40, 2.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4323, 4369], "stddev": [0.0001, 50.0]}) + \
            models.Gaussian1D(2.0, 4101.73, 2.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4078, 4125], "stddev": [0.0001, 50.0]}) + \
            models.Gaussian1D(5.0, 4960.0, 6.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4937, 4983], "stddev": [0.0001, 23.8]}) + \
            models.Gaussian1D(20.0, 5008.0, 6.0, bounds = {"amplitude": [0.0, 50.0], "mean": [4985, 5031], "stddev": [0.0001, 23.8]})
    else:
        hbetan_param = init_value[1][6:9]
        hbetab_param = init_value[1][9:12]
        hother_param = init_value[1][12:18]
        o3_param = init_value[1][18:24]
        hbeta_complex_fit_func = \
                    models.Gaussian1D(hbetan_param[0], hbetan_param[1], hbetan_param[2], bounds = {"amplitude": [0.0, 50.0], "mean": [4830, 4880], "stddev": [0.0001, 10.1]}) + \
                    models.Gaussian1D(hbetab_param[0], hbetab_param[1], hbetab_param[2], bounds = {"amplitude": [0.0, 50.0], "mean": [4830, 4880], "stddev": [10.1, 500.0]}) + \
                    models.Gaussian1D(hother_param[0], hother_param[1], hother_param[2], bounds = {"amplitude": [0.0, 50.0], "mean": [4323, 4369], "stddev": [0.0001, 50.0]}) + \
                    models.Gaussian1D(hother_param[3], hother_param[4], hother_param[5], bounds = {"amplitude": [0.0, 50.0], "mean": [4078, 4125], "stddev": [0.0001, 50.0]}) + \
                    models.Gaussian1D(o3_param[0], o3_param[1], o3_param[2], bounds = {"amplitude": [0.0, 50.0], "mean": [4937, 4983], "stddev": [0.0001, 23.8]}) + \
                    models.Gaussian1D(o3_param[3], o3_param[4], o3_param[5], bounds = {"amplitude": [0.0, 50.0], "mean": [4985, 5031], "stddev": [0.0001, 23.8]})
    fitter = fitting.LevMarLSQFitter()
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            fit = fitter(hbeta_complex_fit_func, wave, flux, weights = error ** (-2), maxiter = 3000)
        except Exception as reason:
            if image_control:  # Control image output
                save_fig(fig1, img_directory, str(mjd) + "-failed")
                plt.close()
            raise SpectraException("Fit failed because of " + str(reason))
    expected = np.array(fit(wave))
    if image_control:  # Control image output
        plt.plot(wave, expected)
        save_fig(fig1, img_directory, str(mjd) + "-succeed")
        plt.close()
    rcs = 0
    for i in range(len(flux)):
        rcs = rcs + (flux[i] - expected[i]) ** 2.0
    rcs = rcs / np.abs(len(flux)-23)
    if rcs > 10.0:
        raise SpectraException("Reduced chi-square too large: " + str(rcs))
    return fit.parameters, cont_fit.parameters, rcs, cont_fitter.fit_info['nfev'], fitter.fit_info['nfev']


# Function to output fit result
def output_fit(fit_result, rmid, mjd, band):
    picklefile = open(Location.project_loca + "result/fit_with_temp/data/" +\
                      str(rmid) + "/" + str(mjd) + "-" + band + ".pkl", "wb")
    pickle.dump(fit_result, picklefile)
    picklefile.close()


# Exception logging process
def exception_logging(rmid, mjd, reason):
    log = open(Location.project_loca + "Fe2_fit_error.log", "a")
    log.write(str(rmid) + " " + str(mjd) + " " + str(reason) + "\n")
    log.close()


# Reduced chisquare logging
def rcs_logging(rmid, rcs):
    log = open(Location.project_loca + "result/fit_with_temp/data/" + str(rmid) + "/rcs.pkl", "wb")
    pickle.dump(rcs, log)
    log.close()


# Individual working process
def fe_fitter_single(rmid, lock, rcs_dict, mjd):
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
        [fit_res, cont_res, rcs] = template_fit(wave, flux, error, True, [],
                                                rmid, mjd)
    except SpectraException as reason:
        lock.acquire()
        exception_logging(rmid, mjd, reason)
        print("Failed for " + str(mjd))
        lock.release()
        return
    output_fit(fit_res, rmid, mjd, "Fe2")
    output_fit(cont_res, rmid, mjd, "cont")
    lock.acquire()
    rcs_dict[mjd] = rcs
    print("Finished for " + str(mjd))
    lock.release()


def fe_fitter(rmid):
    print("Beginning process for " + str(rmid))
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" + str(rmid)))
    pool = Pool(processes = 32)
    m = Manager()
    lock = m.Lock()
    rcs_dict = m.dict()
    f = partial(fe_fitter_single, rmid, lock, rcs_dict)
    pool.map(f, mjd_list)
    rcs_logging(rmid, dict(rcs_dict))
    pool.close()
    pool.join()
