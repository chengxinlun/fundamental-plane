import os
import numpy as np
import pickle
from position import Location
import matplotlib.pyplot as plt
from astropy.modeling import models
from base import get_total_rmid_list, extract_fit_part, read_raw_data, \
    mask_points


def get_flux(rmid, band):
    fe_loc = Location.project_loca + "result/flux_of_line/" + str(rmid) + \
        "/" + str(band) + ".pkl"
    fe_err_loc = Location.project_loca + "result/flux_of_line/" + str(rmid) + \
        "/" + str(band) + "_error.pkl"
    fe_file = open(fe_loc, "rb")
    fe_flux = pickle.load(fe_file)
    fe_file.close()
    fe_err_file = open(fe_err_loc, "rb")
    fe_err = pickle.load(fe_err_file)
    fe_err_file.close()
    return [fe_flux, fe_err]


def intersect(a, b, c, d):
    res_date = set(a.keys()).intersection(set(b.keys()), set(c.keys()),
                                          set(d.keys()))
    mean_a = np.mean([a[x] for x in res_date])
    mean_b = np.mean([a[x] * b[x] for x in res_date])
    mean_c = np.mean([c[x] for x in res_date])
    mean_d = np.mean([c[x] * d[x] for x in res_date])
    return [mean_a, mean_b, mean_c, mean_d]


def get_fe_hb(rmid):
    fe, fe_e = get_flux(rmid, "Fe2")
    hb, hb_e = get_flux(rmid, "Hbetab")
    return intersect(fe, fe_e, hb, hb_e)


def find_wave(wave, flux, index):
    return wave[(np.abs(flux - index)).argmin()]


def get_fwhm_hb(rmid, mjd):
    day_dir = Location.project_loca + "result/fit_with_temp/data/" + \
        str(rmid) + "/" + str(mjd) + "-"
    hb_file = open(day_dir + "Fe2.pkl", "rb")
    hb = pickle.load(hb_file)[10:12]
    hb_file.close()
    cont_file = open(day_dir + "cont.pkl", "rb")
    cont = pickle.load(cont_file)
    cont_file.close()
    cont_func = models.PowerLaw1D(cont[0], cont[1], cont[2])
    [wave, flux, error] = read_raw_data(rmid, mjd)
    [wave, flux, error] = extract_fit_part(wave, flux, error,
                                           hb[0] - 2.0 * hb[1],
                                           hb[0] + 2.0 * hb[1])
    [wave, flux, error] = mask_points(wave, flux, error)
    flux = flux - cont_func(wave)
    up_wave = wave[0:flux.argmax()]
    up_flux = flux[0:flux.argmax()]
    down_flux = flux[flux.argmax():-1]
    down_wave = wave[flux.argmax():-1]
    wave_min = find_wave(up_wave, up_flux, 0.5 * np.amax(flux))
    wave_max = find_wave(down_wave, down_flux, 0.5 * np.amax(flux))
    return (wave_max - wave_min) / hb[1]


rmid_list = get_total_rmid_list()
fe = list()
fe_e = list()
hb = list()
hb_e = list()
for each in rmid_list:
    try:
        a, b, e, f = get_fe_hb(each)
        mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" +
                                       str(each)))
        hb_fwhm = list()
        for each_day in mjd_list:
            hb_fwhm.append(get_fwhm_hb(each, each_day))
    except ValueError as reason:
        continue
    except IOError as reason:
        continue
    fe_e.append((e * b - f * a) / (e * e))
    fe.append(a / e)
    hb.append(np.mean(hb_fwhm))
    hb_e.append(np.std(hb_fwhm))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel("Fe / Hbeta")
ax.set_ylabel("Line profile")
plt.scatter(fe, hb)
plt.errorbar(fe, hb, xerr=fe_e, yerr=hb_e, linestyle='None')
plt.show()
