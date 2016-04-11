import pickle
import os
import numpy as np
from fe_temp_observed import FeII_template_obs
from astropy.modeling import models
from position import Location
from functools import partial
from multiprocessing import Manager, Pool


class FileNotFound(Exception):
    pass


# Read in the fit result
def read_fit_res(rmid, mjd, band):
    try:
        data_file = open(
            Location.project_loca +
            "/result/fit_with_temp/data/" +
            str(rmid) +
            "/" +
            str(mjd) +
            "-" +
            str(band) +
            ".pkl",
            "rb")
    except Exception:
        raise FileNotFound
    res = pickle.load(data_file)
    data_file.close()
    return res


# Integrate to get flux
def calc_flux(res, cont_res):
    # Separate the parameter and construct integrating function
    fe2_func = FeII_template_obs(
        res[0],
        res[1],
        res[2],
        res[3],
        res[4],
        res[5])
    cont_func = models.PowerLaw1D(cont_res[0], cont_res[1], cont_res[2])
    # Integrate to get flux
    x = np.linspace(4000.0, 5500.0, 100000)
    fe2_flux = np.trapz(fe2_func(x), x)
    cont_flux = cont_func(5100.0)
    hbetan_flux = np.sqrt(2.0 * np.pi) * abs(res[8]) * res[6]
    hbetab_flux = np.sqrt(2.0 * np.pi) * abs(res[11]) * res[9]
    o3_flux = np.sqrt(2.0 * np.pi) * abs(res[23]) * res[21]
    return [fe2_flux, hbetan_flux, hbetab_flux, o3_flux, cont_flux]


# Output calculation result
def output_flux(rmid, dic, band):
    fileout = open(Location.project_loca + "result/flux_of_line/" + str(rmid) +
                   "/" + str(band) + ".pkl", "wb")
    pickle.dump(dic, fileout)
    fileout.close()


# Integrate line for specified rmid in mjd
def line_integration_single(rmid, lock, fe2dic, hbetandic, hbetabdic, o3dic,
                            contdic, mjd):
    res = []
    try:
        res = read_fit_res(rmid, mjd, "Fe2")
    except FileNotFound:
        lock.acquire()
        print("Fit file not found: " + str(rmid) + " " + str(mjd))
        lock.release()
        return
    try:
        cont_res = read_fit_res(rmid, mjd, "cont")
    except FileNotFound:
        lock.acquire()
        print("Continuum file not found: " + str(rmid) + " " + str(mjd))
        lock.release()
        return
    [fe2, hbetan, hbetab, o3, cont] = calc_flux(res, cont_res)
    fe2dic[mjd] = fe2
    hbetandic[mjd] = hbetan
    hbetabdic[mjd] = hbetab
    o3dic[mjd] = o3
    contdic[mjd] = cont


# Interface
def line_integration(rmid):
    print("Begin process for " + str(rmid))
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" +
                                   str(rmid)))
    pool = Pool(processes=32)
    m = Manager()
    lock = m.Lock()
    fe2dic = m.dict()
    hbetandic = m.dict()
    hbetabdic = m.dict()
    o3dic = m.dict()
    contdic = m.dict()
    func = partial(line_integration_single, rmid, lock, fe2dic, hbetandic,
                   hbetabdic, o3dic, contdic)
    pool.map(func, mjd_list)
    output_flux(rmid, dict(fe2dic), "Fe2")
    output_flux(rmid, dict(hbetandic), "Hbetan")
    output_flux(rmid, dict(hbetabdic), "Hbetab")
    output_flux(rmid, dict(contdic), "cont")
    output_flux(rmid, dict(o3dic), "O3")
    pool.close()
    pool.join()
