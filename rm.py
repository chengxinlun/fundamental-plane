import numpy
import os
import pickle
from position import Location

def read_flux(rmid, band):
    f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" + str(band) + ".pkl", "rb")
    dic = pickle.load(f)
    return dic


def 

