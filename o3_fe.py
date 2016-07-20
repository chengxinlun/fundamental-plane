import numpy as np
import pickle
from position import Location
import matplotlib.pyplot as plt
from base import get_total_rmid_list


def get_flux(rmid, band):
    fe_loc = Location.project_loca + "result/flux_of_line/" + str(rmid) + \
        "/" + str(band) + ".pkl"
    fe_err_loc = Location.project_loca + "result/flux_of_line/" + str(rmid) + \
        "/" + str(band) + "_error.pkl"
    fe_file = open(fe_loc, "rb")
    fe_flux = pickle.load(fe_file)
    fe_file.close()
    fe_err_file = open(fe_err_loc, "rb")
    fe_err = pickle.load(fe_err_file)
    fe_err_file.close()
    return [fe_flux, fe_err]


def intersect(a, b, c, d, e, f):
    res_date = set(a.keys()).intersection(set(b.keys()), set(c.keys()),
                                          set(d.keys()), set(e.keys()),
                                          set(f.keys()))
    mean_a = np.mean([a[x] for x in res_date])
    mean_b = np.mean([a[x] * b[x] for x in res_date])
    mean_c = np.mean([c[x] for x in res_date])
    mean_d = np.mean([c[x] * d[x] for x in res_date])
    mean_e = np.mean([e[x] for x in res_date])
    mean_f = np.mean([e[x] * f[x] for x in res_date])
    return [mean_a, mean_b, mean_c, mean_d, mean_e, mean_f]


def get_fe_hb(rmid):
    fe, fe_e = get_flux(rmid, "Fe2")
    hb, hb_e = get_flux(rmid, "Hbetab")
    o3, o3_e = get_flux(rmid, "O3")
    return intersect(fe, fe_e, o3, o3_e, hb, hb_e)


rmid_list = get_total_rmid_list()
fe = list()
fe_e = list()
hb = list()
hb_e = list()
for each in rmid_list:
    a, b, c, d, e, f = get_fe_hb(each)
    fe.append(a / e)
    fe_e.append((e * b - f * a) / (e * e))
    hb.append(c / e)
    hb_e.append((e * d - f * c) / (e * e))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel("Fe / Hbeta")
ax.set_ylabel("OIII / Hbeta")
plt.scatter(fe, hb)
plt.errorbar(fe, hb, xerr=fe_e, yerr=hb_e, linestyle='None')
plt.show()
