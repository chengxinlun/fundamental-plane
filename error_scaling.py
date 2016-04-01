import pickle
from position import Location
from base import read_raw_data
from functools import partial
from multiprocessing import Manager, Pool


def read_rcs(rmid):
    f = open(Location.project_loca + "result/fit_with_temp/data/" + str(rmid) +
             "/rcs.pkl")
    rcs_dict = pickle.load(f)
    f.close()
    return rcs_dict


def error_scaling_single(lock, rcs_dict, rmid, mjd):
    [wave, flux, error] = read_raw_data(rmid, int(mjd))
    error = error * rcs_dict[mjd]
    f = open(Location.project_loca + "data/raw/" + str(rmid) + "/" +
             str(mjd) + "/" + "error_scaled.pkl", "wb")
    pickle.dump(error, f)
    lock.acquire()
    print("Error scaling finished for " + str(mjd))
    lock.release()


def error_scaling(rmid):
    rcs_dict = read_rcs(rmid)
    p = Pool(processes = 32)
    m = Manager()
    l = m.Lock()
    func = partial(error_scaling_single, l, rcs_dict, rmid)
    p.map(func, rcs_dict.keys())
    p.close()
    p.join()
    print("Finished for " + str(rmid) + "\n\n")
