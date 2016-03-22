import pickle
import numpy as np
from base import read_raw_data, mask_points, extract_fit_part
from fe_temp_observed import FeII_template_obs


def get_error(center, width, wave, flux, error):
    [wavea, fluxa, errora] = extract_fit_part(wave, flux, error, ceter - 2.0 * width, center + 2.0 * width)
    re = np.sum((errora ** 2) / (wavea ** 2))
    return re


def estimate_error_single(rmid, mjd):
    [wave, flux, error] = read_raw_data(rmid, mjd)
    [wave, flux, error] = mask_points(wave, flux, error)
    fe_temp = FeII_template_obs(res[0], res[1], res[2], res[3], res[4], res[5])

