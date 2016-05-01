import numpy
import os
import pickle
from position import Location

def read_flux(rmid, band):
    f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" + str(band) + ".pkl", "rb")
    dic = pickle.load(f)
    return dic


def read_re(rmid, band):
    f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" + str(band) + "-error.pkl", "rb")
    dic =pickle.load(f)
    return dic


def lc_gene(rmid):
    band_list = ["hbeta", "o3", "cont"]
    for each in band_list:
        flux = read_flux(rmid, each)
        error = read_re(rmid, each)
        all_mjd = list()
        all_mjd.extend(flux.keys())
        all_mjd.extend(error.keys())
        mjd_list = sorted(set(all_mjd))
        lc = list()
        err = list()
        for each_day in mjd_list:
            lc.append(flux[each])
            err.append(flux[each] * error[each])
