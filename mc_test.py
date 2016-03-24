import os
import numpy as np
from fe_fitter import template_fit
from multiprocessing import Pool, Manager

def noise_gene(flux, error):
    noise = np.array([])
    for i in range(len(error)):
        np.append(noise, np.random.normal(flux[i], error[i], 100))
    noise = np.tile(flux, [100, 1]) + np.transpose(noise)
    return noise

def get_error(rmid, mjd):
    pool = Pool(processes = 4)

