import numpy as np
import pickle
from fe_fitter import template_fit
from base import read_raw_data, mask_points, extract_fit_part
from line_integration import calc_flux
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
    res = template_fit(wave, flux, error, rmid, str(mjd) + "-" + str(num))
    line_flux = calc_flux(res[0], res[1])
    fit_res.append(line_flux)


def mc_test_single(rmid, mjd):
    [wave, flux, error] = read_raw_data(rmid, mjd)
    error = pickle.load(open(Location.project_loca + "data/raw/" + str(rmid) +
                             "/" + str(mjd) + "/" + "error_scaled.pkl", "rb"))
    [wave, flux, error] = mask_points(wave, flux, error)
    [wave, flux, error] = extract_fit_part(wave, flux, error, 4000.0, 5500.0)
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
    print(std_res)
    print(mean_res)
