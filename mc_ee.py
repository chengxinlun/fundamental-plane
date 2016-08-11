import os
import time
import numpy as np
import pickle
from fe_fitter import template_fit
from base import read_raw_data, mask_points, extract_fit_part
from line_integration import calc_flux, output_flux
from multiprocessing import Pool, Manager
from functools import partial
from position import Location


def noise_gene(flux, error):
    noise = list()
    for i in range(len(error)):
        noise.append(np.random.normal(flux[i], error[i], 100))
    noise = np.array(noise)
    noise = np.transpose(noise)
    return noise


def get_flux(wave, rmid, mjd, fit_res, args):
    flux = args[0]
    error = args[1]
    num = args[2]
    try:
        cont_result = pickle.load(open(Location.project_loca +
                                       "result/fit_with_temp/data/" +
                                       str(rmid) + "/" + str(mjd) + "-cont.pkl",
                                       "rb"))
        fit_result = pickle.load(open(Location.project_loca +
                                      "result/fit_with_temp/data/" + str(rmid) +
                                      "/" + str(mjd) + "-Fe2.pkl", "rb"))
    except Exception:
        return
    init = [cont_result, fit_result]
    try:
        res = template_fit(wave, flux, error, False, init, rmid, str(mjd) +
                           "-" + str(num))
    except Exception:
        return
    line_flux = calc_flux(res[0], res[1])
    fit_res.append(line_flux)


def mc_ee_single(rmid, mjd):
    print("    Begin for " + str(mjd))
    try:
        [wave, flux, error] = read_raw_data(rmid, mjd)
        # error = pickle.load(open(Location.project_loca + "data/raw/" +
        #                          str(rmid) + "/" + str(mjd) + "/" +
        #                          "error_scaled.pkl", "rb"))
        [wave, flux, error] = mask_points(wave, flux, error)
        [wave, flux, error] = extract_fit_part(wave, flux, error, 4000.0,
                                               5500.0)
    except Exception:
        print("        Unable to locate data file.")
        return [[], []]
    flux_with_noise = noise_gene(flux, error)
    error_with_noise = np.tile(error, [100, 1])
    num_list = list(range(100))
    m = Manager()
    p = Pool(processes=100)
    fit_res = m.list()
    func = partial(get_flux, wave, rmid, mjd, fit_res)
    args = list()
    for i in range(len(flux_with_noise)):
        args.append([flux_with_noise[i], error_with_noise[i], num_list[i]])
    p.map(func, args)
    p.close()
    res = np.transpose(np.array(list(fit_res)))
    std_res = list()
    mean_res = list()
    for each in res:
        std_res.append(np.std(each))
        mean_res.append(np.mean(each))
    return [std_res, mean_res]


def mc_ee(rmid):
    print("Begin mc error estimation for " + str(rmid))
    start_t = time.time()
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" +
                                   str(rmid)))
    fe2edic = dict()
    hbetabedic = dict()
    hbetanedic = dict()
    o3edic = dict()
    contedic = dict()
    for each in mjd_list:
        [std_res, mean_res] = mc_ee_single(rmid, each)
        try:
            fe2edic[each] = std_res[0] / mean_res[0]
        except Exception:
            pass
        try:
            hbetanedic[each] = std_res[1] / mean_res[1]
        except Exception:
            pass
        try:
            hbetabedic[each] = std_res[2] / mean_res[2]
        except Exception:
            pass
        try:
            o3edic[each] = std_res[3] / mean_res[3]
        except Exception:
            pass
        try:
            contedic[each] = std_res[4] / mean_res[4]
        except Exception:
            pass
    output_flux(rmid, fe2edic, "Fe2_error")
    output_flux(rmid, hbetabedic, "Hbetab_error")
    output_flux(rmid, hbetanedic, "Hbetan_error")
    output_flux(rmid, o3edic, "O3_error")
    output_flux(rmid, contedic, "cont_error")
    print("Time elapsed: " + str(time.time()-start_t) + " seconds")
    print("Finished \n\n")
