import os
import pickle
import numpy as np
from base import read_raw_data, mask_points, extract_fit_part, read_database,\
    union
from fe_temp_observed import FeII_template_obs
from position import Location
from functools import partial
from multiprocessing import Manager, Pool


def get_error(center, width, wave, flux, error):
    [wavea, fluxa, errora] = extract_fit_part(wave, flux, error,
                                              center - 2.0 * width,
                                              center + 2.0 * width)
    re = np.sum((errora ** 2) / (fluxa ** 2))
    return np.sqrt(re)


def get_fe2_re(fit_res, wave, flux, error):
    width_l1 = fit_res[1] * np.sqrt(3 / 2) / 299792.458
    width_n3 = fit_res[4] * np.sqrt(3 / 2) / 299792.458
    line_list = list()
    for each in FeII_template_obs.center_l1:
        line_list.append([each - 2.0 * width_l1 * each, each + 2.0 * width_l1 *
                         each])
    for each in FeII_template_obs.center_n3:
        line_list.append([each - 2.0 * width_n3 * each, each + 2.0 * width_n3 *
                         each])
    total_line = union(line_list)
    re = 0.0
    for each in total_line:
        temp = get_error(np.mean(each), (each[1] - each[0]) * 0.25, wave, flux,
                         error)
        re = re + temp ** 2.0
    return np.sqrt(re)


def estimate_error_single(rmid, hbetab_dic, hbetan_dic, o3_dic, fe2_dic, mjd):
    [wave, flux, error] = read_raw_data(rmid, mjd)
    error = pickle.load(open(Location.project_loca + "data/raw/" + str(rmid) +
                             "/" + str(mjd) + "/" + "error_scaled.pkl", "rb"))
    [wave, flux, error] = extract_fit_part(wave, flux, error, 4000.0, 5500.0)
    [wave, flux, error] = mask_points(wave, flux, error)
    try:
        res = read_database(Location.project_loca +
                            "result/fit_with_temp/data/" +
                            str(rmid) + "/" + str(mjd) + "-Fe2.pkl")
    except OSError:
        return
    fe_temp = np.vectorize(FeII_template_obs(res[0], res[1], res[2], res[3],
                                             res[4], res[5]))
    flux_fe = fe_temp(wave)
    print(flux_fe)
    flux_no_fe = flux - flux_fe
    hbetab_re = get_error(res[10], res[11], wave, flux_no_fe, error)
    hbetan_re = get_error(res[7], res[8], wave, flux_no_fe, error)
    o3_re = get_error(res[19], res[20], wave, flux_no_fe, error)
    fe2_re = get_fe2_re(res, wave, flux_fe, error)
    hbetab_dic[mjd] = hbetab_re
    hbetan_dic[mjd] = hbetan_re
    o3_dic[mjd] = o3_re
    fe2_dic[mjd] = fe2_re
    print(hbetab_dic)
    print(hbetan_dic)
    print(o3_dic)
    print(fe2_dic)


def error_estimate(rmid):
    p = Pool(processes=32)
    m = Manager()
    hb = m.dict()
    hn = m.dict()
    o3 = m.dict()
    fe2 = m.dict()
    func = partial(estimate_error_single, rmid, hb, hn, o3, fe2)
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" +
                                   str(rmid)))
    p.map(func, mjd_list)

m = Manager()
hb = m.dict()
hn = m.dict()
o3 = m.dict()
fe2 = m.dict()
estimate_error_single(1141, hb, hn, o3, fe2, 56660)
