import pickle
import numpy as np
from fe_temp_observed import FeII_template_obs
from astropy.modeling import models
import matplotlib.pyplot as plt
from position import Location


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
def calc_flux(res):
    # Separate the parameter and construct integrating function
    fe2_func = FeII_template_obs(
        res[0],
        res[1],
        res[2],
        res[3],
        res[4],
        res[5])
    # Integrate to get flux
    x = np.linspace(4000.0, 5500.0, 100000)
    fe2_flux = np.trapz(fe2_func(x), x)
    hbetan_flux = np.sqrt(2.0 * np.pi) * abs(res[8]) * res[6]
    hbetab_flux = np.sqrt(2.0 * np.pi) * abs(res[10]) * res[11]
    return [fe2_flux, hbetan_flux, hbetab_flux]


# Output calculation result
def output_flux(rmid, dic, band):
    fileout = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" + str(band) + ".pkl", "wb")
    pickle.dump(dic, fileout)
    fileout.close()


# Integrate line for specified rmid in mjd
def line_integration_single(rmid, lock, fe2dic, hbetandic, hbetabdic, mjd):
    try:
        res = read_fit_res(rmid, mjd)
    except FileNotFound:
        lock.acquire()
        print("Fit file not found: " + str(rmid) + " " + str(mjd))
        lock.release()
    [fe2, hbetan, hbetab] = calc_flux(res)
    fe2dic[mjd] = fe2
    hbetan[mjd] = hbetan
    hbetab[mjd] = hbetab


def line_integration(rmid):
    fe2dic = dict()
    hbetandic = dict()
    hbetabdic = dict()
    print("Begin process for " + str(rmid))
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" + str(rmid)))
