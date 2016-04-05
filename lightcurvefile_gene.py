import os
import pickle
from position import Location


def unipicklereader(filename):
    f = open(filename, "wb")
    res = pickle.load(f)
    return res


def lcgen_single(rmid, mjd):


