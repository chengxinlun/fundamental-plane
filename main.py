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
    already = [238, 909, 1202, 497, 559, 1043, 238, 917, 1106, 1094, 569, 742, 29, 456,
               905, 946, 1212, 607, 1101, 51, 423, 405, 980, 732, 379, 1213, 1103, 469,
               866, 887, 370, 936, 1078, 925, 437, 76, 1039, 783, 131, 337, 351, 1087,
               1098, 418, 527, 844, 149, 1210, 416, 450, 151, 656, 1021, 1122, 1055,
               1052, 259, 269, 377, 1149, 518, 225, 118, 1137, 371, 1076, 637, 1105,
               1165, 1207, 786, 1128, 992, 1099, 373, 1088, 127, 1089, 664]
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        if each in already:
            continue
        mc_ee(each)


error_estimation_all()
print("ALL FINISHED")
