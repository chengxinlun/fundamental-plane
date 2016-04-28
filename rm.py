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
    lc = dict()
    for each in band_list:
        lc[each] =
