# Just run this file to get the result
from base import get_total_rmid_list
# from raw_reader import raw_reader
from fe_fitter import fe_fitter
from line_integration import line_integration
from error_scaling import error_scaling
from binning import binning
from mc_ee import mc_ee
from rm import rm
from hist_fit import hist_fit


def task_splitter(task, num_thread):
    num_per_thread = int(len(task) / num_thread)
    splitted = range(num_thread)
    for i in range(num_thread - 1):
        splitted[i] = task[i * num_per_thread: (i + 1) * num_per_thread]
    splitted[num_thread - 1] = task[(num_thread - 1) * num_per_thread: -1]
    return splitted


def fit_all():
    rmid_list = get_total_rmid_list()
    for i in range(0, len(rmid_list)):
        fe_fitter(rmid_list[i])
        print(str(i + 1) + "out of " + str(len(rmid_list)))
        print("\n\n")


def inte_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        try:
            line_integration(each)
        except Exception as reason:
            print("Failed because of: " + str(reason))


def bin_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        binning(each)


def rescale_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        error_scaling(each)


def error_estimation_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        try:
            mc_ee(each)
        except Exception as reason:
            print("Failed because of: " + str(reason))


def rm_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        try:
            rm(each)
        except Exception as reason:
            print("Failed because of: " + str(reason))


def hist_fit_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        hist_fit(each)


inte_all()
error_estimation_all()
rm_all()
hist_fit_all()
