import os
import pickle
from position import Location
from javelin.zylc import get_data
from javelin.lcmodel import Cont_Model, Rmap_Model


def read_flux(rmid, band):
    f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" +
             str(band) + ".pkl", "rb")
    dic = pickle.load(f)
    return dic


def read_re(rmid, band):
    f = open(Location.project_loca + "result/flux_of_line/" + str(rmid) + "/" +
             str(band) + "_error.pkl", "rb")
    dic = pickle.load(f)
    return dic


def lc_gene(rmid):
    band_list = ["Hbetab", "O3", "cont"]
    for each in band_list:
        flux = read_flux(rmid, each)
        error = read_re(rmid, each)
        flux_key = set(flux.keys())
        error_key = set(error.keys())
        print(flux)
        print(error)
        all_mjd = flux_key.intersection(error_key)
        mjd_list = sorted(all_mjd)
        lc_file = open(Location.project_loca + "result/light_curve/" +
                       str(rmid) + "/" + str(each) + ".txt", "w")
        for each_day in mjd_list:
            lc_file.write(str(each_day) + "    " + str(flux[each_day]) +
                          "    " + str(flux[each_day] * error[each_day]) + "\n")
        lc_file.close()


def rm_single(rmid):
    file_con = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/cont.txt"
    file_hbeta = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/Hbetab.txt"
    c = get_data([file_con])
    cmod = Cont_Model(c)
    cmod.do_mcmc(threads=10)
    cy = get_data([file_con, file_hbeta])
    cy.plot()
    cymod = Rmap_Model(cy)
    data_out = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/cont-hbeta.txt"
    cymod.do_mcmc(conthpd=cmod.hpd, threads=10, fchain=data_out)
    fig_out = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "cont-hbeta"
    cymod.show_hist(figout=fig_out, figext="png")


def rm(rmid):
    print("Begin rm for " + str(rmid))
    os.chdir(Location.project_loca + "result")
    try:
        os.mkdir("light_curve")
    except OSError:
        pass
    os.chdir("light_curve")
    try:
        os.mkdir(str(rmid))
    except OSError:
        pass
    # try:
    lc_gene(rmid)
    rm_single(rmid)
    print("    Finished")
    # except Exception as reason:
    #    print("    Failed because of: " + str(reason))
