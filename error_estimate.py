import pickle
import numpy as np
from base import read_raw_data, mask_points, extract_fit_part, read_database
from fe_temp_observed import FeII_template_obs
from position import Location
import time


def get_error(center, width, wave, flux, error):
    [wavea, fluxa, errora] = extract_fit_part(wave, flux, error, center - 2.0 * width, center + 2.0 * width)
    re = np.sum((errora ** 2) / (wavea ** 2))
    return np.sqrt(re)


def estimate_error_single(rmid, hbetab_dic, hbetan_dic, o3_dic, fe2_dic, mjd):
    [wave, flux, error] = read_raw_data(rmid, mjd)
    [wave, flux, error] = extract_fit_part(wave, flux, error, 4000.0, 5500.0)
    [wave, flux, error] = mask_points(wave, flux, error)
    res = read_database(Location.project_loca + "result/fit_with_temp/data/" + str(rmid) + "/" + str(mjd) + "-Fe2.pkl")
    fe_temp = np.vectorize(FeII_template_obs(res[0], res[1], res[2], res[3], res[4], res[5]))
    flux_fe = fe_temp(wave)
    flux_no_fe = flux - flux_fe
    hbetab_re = get_error(res[10], res[11], wave, flux_no_fe, error)
    hbetan_re = get_error(res[7], res[8], wave, flux_no_fe, error)
    o3_re = get_error(res[19], res[20], wave, flux_no_fe, error)
    fe2_re = get_error(4750.0, 375.0, wave, flux_fe, error)
    hbetab_dic[mjd] = hbetab_re
    hbetan_dic[mjd] = hbetan_re
    o3_dic[mjd] = o3_re
    fe2_dic[mjd] = fe2_re

hb = dict()
hn = dict()
o3 = dict()
fe2 = dict()
estimate_error_single(1141, hb, hn, o3, fe2, 56660)
print(hb)
print(hn)
print(o3)
print(fe2)
