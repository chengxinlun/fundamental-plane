# Just run this file to get the result
from base import get_total_rmid_list
# from raw_reader import raw_reader
from fe_fitter import fe_fitter
from line_integration import line_integration
from error_scaling import error_scaling
from binning import binning
from mc_ee import mc_ee


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
        line_integration(each)


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
        mc_ee(each)


fit_all()
print("Fit finished")
inte_all()
print("Flux finished")
rescale_all()
print("Rescale finished")
error_estimation_all()
print("ALL FINISHED")
