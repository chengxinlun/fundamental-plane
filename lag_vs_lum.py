import os
import pickle
import numpy as np
from astropy.modeling import models, fitting
from astropy.cosmology import FlatLambdaCDM
import matplotlib.pyplot as plt
from base import get_total_rmid_list
from position import Location


def get_raw_lum(rmid):
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" +
                                   str(rmid)))
    try:
        f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) +
                 "/cont_error.pkl")
        cont_err = pickle.load(f)
        f.close()
        err = max(cont_err.values())
    except Exception:
        raise
    lum = 0.0
    num = 0.0
    for each in mjd_list:
        try:
            f = open(Location.project_loca + "result/fit_with_temp/data/" +
                     str(rmid) + "/" + str(each) + "-cont.pkl", "rb")
            cont_res = pickle.load(f)
            f.close()
            cont_func = models.PowerLaw1D(cont_res[0], cont_res[1], cont_res[2])
            num = num + 1.0
            lum = lum + cont_func(5100.0)
        except Exception:
            continue
    return [lum / num, err]


def get_lum(rmid, zfinal_dict):
    flux = get_raw_lum(rmid)
    z = zfinal_dict[int(rmid)]
    cosmo = FlatLambdaCDM(H0=70.0, Om0=0.3)
    dl_MPC = cosmo.luminosity_distance(z)
    dl_cm = float(dl_MPC.value * 3.085677581 * (10.0 ** 24.0))
    lum = 4.0 * 3.1415926 * dl_cm * dl_cm * flux[0] * 10. ** (0. - 17.)
    return [lum, flux[1] * lum]


def get_lag(rmid, zfinal_dict):
    f = open(Location.project_loca + "result/light_curve/" + str(rmid) +
             "/result.pkl")
    raw_lag = pickle.load(f)
    f.close()
    return [10.0 ** raw_lag[0][1], 10.0 ** raw_lag[1][1]]


def plot_lum_vs_lag():
    rmid_list = get_total_rmid_list()
    zfinal = pickle.load(open(Location.project_loca +
                              "/info_database/zfinal.pkl"))
    lag_list = list()
    lag_err_list = list()
    lum_list = list()
    lum_err_list = list()
    fig = plt.figure()
    for each in rmid_list:
        if each in [259]:
            continue
        try:
            lag, lag_err = get_lag(each, zfinal)
            lag_list.append(lag)
            lag_err_list.append(lag_err)
            lum, lum_err = get_lum(each, zfinal)
            lum_list.append(lum)
            lum_err_list.append(lum_err)
        except Exception:
            continue
        # plt.errorbar([lum], [lag])
        # fig.text(np.log10(lum), np.log10(lag), str(each))
    lag = np.log10(np.array(lag_list))
    lum = np.log10(np.array(lum_list))
    lag_err = np.array(lag_err_list) / np.array(lag_list)
    lum_err = np.array(lum_err_list) / np.array(lum_list)
    theory = models.Linear1D(0.5, -10.0, fixed={"slope": True})
    obs = models.Const1D(0.0)
    fitter = fitting.LinearLSQFitter()
    theory_fit = fitter(theory, lum, lag, weights = lag_err ** 2.0)
    print(theory_fit.parameters)
    obs_fit = fitter(obs, lum, lag, weights = lag_err ** 2.0)
    print(obs_fit.parameters)
    rcs = np.sum((obs_fit(lum) - lag) ** 2.0) ** 0.5 / (len(rmid_list) - 1.0)
    print(rcs)
    plt.errorbar(lum, lag, xerr=lum_err, yerr=lag_err, fmt='o')
    # plt.plot(lum, theory_fit(lum))
    plt.plot(lum, obs_fit(lum))
    plt.show()


plot_lum_vs_lag()
