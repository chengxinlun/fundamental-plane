import pickle
from position import Location
from base import read_raw_data


def read_rcs(rmid):
    f = open(Location.project_loca + "result/fit_with_temp/data/" + str(rmid) +
             "/rcs.pkl")
    rcs_dict = pickle.load(f)
    f.close()
    return rcs_dict


def error_scaling_single(lock, rmid):
    rcs_dict = read_rcs(rmid)
    for each in rcs_dict.keys():
        [wave, flux, error] = read_raw_data(rmid, int(each))
        error = error * rcs_dict[each]
        f = open(Location.project_loca + "data/raw/" + str(rmid) + "/" +
                 str(each) + "/" + "error_scaled.pkl", "wb")
        pickle.dump(error, f)
    lock.acquire()
    print("Error scaling finished for " + str(rmid))
    lock.release()
