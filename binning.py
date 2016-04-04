import os
import numpy as np
import math
import pickle
from multiprocessing import Pool, Manager
from functools import partial
from position import Location
from base import read_raw_data, mask_points


# Binning adjacent points into one
def binning_point(wave, flux, error):
    new_wave_list = []
    new_error_list = []
    for i in range(100):
        flux_with_error = []
        for j in range(len(error)):
            flux_with_error.append(np.random.normal(0.0, error[j]) + flux[j])
        new_flux = np.sum(flux_with_error)
        new_error_list.append(np.mean(flux_with_error))
        new_wave_list.append(np.sum(flux_with_error * wave) / new_flux)
    return [np.mean(new_wave_list), np.mean(new_error_list),
            np.std(new_error_list)]


# Output the binning result
def output(rmid, mjd, data, name):
    f = open(Location.project_loca + "data/binned/" + str(rmid) + "/" +
             str(mjd) + "/" + name + ".pkl", "wb")
    pickle.dump(data, f)
    f.close()


# Do binning for specified rmid and mjd (5 to 1)
def binning_single(rmid, lock, mjd):
    lock.acquire()
    print("Begin for " + str(mjd))
    lock.release()
    os.chdir(Location.project_loca + "data/binned/" + str(rmid))
    try:
        os.mkdir(str(mjd))
    except OSError:
        pass
    [wave, flux, error] = read_raw_data(rmid, mjd)
    [wave, flux, error] = mask_points(wave, flux, error)
    if len(wave) == 0:
        print("No valid data found for " + str(mjd))
        return
    num = math.ceil(len(wave) / 5.0)
    wave = np.array_split(wave, num)
    flux = np.array_split(flux, num)
    error = np.array_split(error, num)
    new_wave = []
    new_flux = []
    new_error = []
    for i in range(len(wave)):
        [temp1, temp2, temp3] = binning_point(wave[i], flux[i], error[i])
        new_wave.append(temp1)
        new_flux.append(temp2)
        new_error.append(temp3)
    output(rmid, mjd, new_wave, "wave")
    output(rmid, mjd, new_flux, "flux")
    output(rmid, mjd, new_error, "error")
    lock.acquire()
    print("Finished for " + str(mjd))
    lock.release()


# Interface
def binning(rmid):
    print("Beginning process for " + str(rmid))
    mjd_list = map(int, os.listdir(Location.project_loca + "data/raw/" +
                                   str(rmid)))
    os.chdir(Location.project_loca + "data/")
    try:
        os.mkdir("binned")
    except OSError:
        pass
    os.chdir("binned")
    try:
        os.mkdir(str(rmid))
    except OSError:
        pass
    pool = Pool(processes=32)
    m = Manager()
    l = m.Lock()
    func = partial(binning_single, rmid, l)
    pool.map(func, mjd_list)
    pool.close()
    pool.join()
