import numpy
import os
import pickle
from position import Location


def read_flux(rmid, band):
    f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" +
             str(band) + ".pkl", "rb")
    dic = pickle.load(f)
    return dic


def read_re(rmid, band):
    f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" +
             str(band) + "-error.pkl", "rb")
    dic = pickle.load(f)
    return dic


def lc_gene(rmid):
    band_list = ["hbeta", "o3", "cont"]
    for each in band_list:
        try:
            flux = read_flux(rmid, each)
            error = read_re(rmid, each)
        except Exception:
            print("Unable to locate flux or error file. Exiting.")
            return
        all_mjd = list()
        all_mjd.extend(flux.keys())
        all_mjd.extend(error.keys())
        mjd_list = sorted(set(all_mjd))
        lc_file = open(Location.project_loca + "result/light_curve/" +
                       str(rmid) + "/" + str(each) + ".txt", "w")
        for each_day in mjd_list:
            lc_file.write(str(each_day) + "    " + str(flux[each]) + "    " +
                          str(flux[each] * error[each]))
        lc_file.close()
