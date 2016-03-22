# Just run this file to get the result
from base import get_total_rmid_list
from raw_reader import raw_reader
from multiprocessing import Pool
from fe_fitter import fe_fitter
from line_integration import line_integration


def task_splitter(task, num_thread):
    num_per_thread = int(len(task) / num_thread)
    splitted = range(num_thread)
    for i in range(num_thread - 1):
        splitted[i] = task[i * num_per_thread: (i + 1) * num_per_thread]
    splitted[num_thread - 1] = task[(num_thread - 1) * num_per_thread: -1]
    return splitted


def read_all_raw_data():
    rmid_list = get_total_rmid_list()
    # Multiprocess data reading
    workers = Pool(processes = 4)
    workers.map(raw_reader, rmid_list)


def fit_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        fe_fitter(each)

def init_all():
    rmid_list = get_total_rmid_list()
    for each in rmid_list:
        line_integration(rmid)

fe_fitter(1141)
