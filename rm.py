import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
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
    o3_flux = read_flux(rmid, "O3")
    o3_error = read_re(rmid, "O3")
    band_list = ["Hbetab", "O3", "cont"]
    for each in band_list:
        flux = read_flux(rmid, each)
        error = read_re(rmid, each)
        flux_key = set(flux.keys())
        error_key = set(error.keys())
        all_mjd = flux_key.intersection(error_key)
        mjd_list = sorted(all_mjd)
        lc_file = open(Location.project_loca + "result/light_curve/" +
                       str(rmid) + "/" + str(each) + ".txt", "w")
        for each_day in mjd_list:
            try:
                flux_each = flux[each_day] / o3_flux[each_day]
                error_each = abs(error[each_day] * flux[each_day] *
                                 o3_flux[each_day] - o3_error[each_day] *
                                 o3_flux[each_day] * flux[each_day]) / \
                    (o3_flux[each_day] ** 2.0)
            except Exception:
                continue
            lc_file.write(str(each_day) + "    " + str(flux_each) + "    " +
                          str(error_each) + "\n")
        lc_file.close()


def rm_single(rmid, nwalker, nchain, nburn, min_lag, max_lag, fig_out):
    # Input and output data position and name
    file_con = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/cont.txt"
    file_hbeta = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/Hbetab.txt"
    lc_plot = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/lightcurve"
    data_out = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/cont-hbeta.txt"
    last_mcmc = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/last_mcmc"
    # Fit continuum
    c = get_data([file_con])
    cmod = Cont_Model(c)
    cmod.do_mcmc(threads=100, nwalkers=nwalker, nchain=nchain, nburn=nburn)
    # Do mcmc
    cy = get_data([file_con, file_hbeta], names=["Continuum", "Hbeta"])
    cy.plot(figout=lc_plot, figext="png")
    cymod = Rmap_Model(cy)
    cymod.do_mcmc(conthpd=cmod.hpd, threads=100, fchain=data_out,
                  nwalkers=nwalker, nchain=2.0 * nchain, nburn=2.0 * nburn,
                  laglimit=[[min_lag, max_lag]])
    # Output mcmc result
    cymod.show_hist(figout=fig_out, figext="png")
    cypred = cymod.do_pred()
    cypred.plot(set_pred=True, obs=cy, figout=last_mcmc, figext="png")
    return cymod.get_hpd()


def rm(rmid, nwalker=500, nchain=250, nburn=250, ** kwargs):
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
    try:
        lc_gene(rmid)
        fig_out = Location.project_loca + "result/light_curve/" + str(rmid) + \
            "/cont-hbeta"
        if "outname" in kwargs:
            fig_out = fig_out + "-" + str(kwargs["outname"])
        min_lag = 0.0
        max_lag = 500.0
        print(rm_single(rmid, nwalker, nchain, nburn, min_lag, max_lag, fig_out))
        print("    Finished")
    except Exception as reason:
        print("    Failed because of: " + str(reason))
