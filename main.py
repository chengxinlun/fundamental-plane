from base import get_total_rmid_list
from raw_reader import raw_reader
from multiprocessing import Pool

def task_splitter(task, num_thread):
    num_per_thread = int(len(task) / num_thread)
    splitted = range(num_thread)
    for i in range(num_thread - 1):
        splitted[i] = task[i * num_per_thread: (i + 1) * num_per_thread]
    splitted[num_thread - 1] = task[(num_thread - 1) * num_per_thread: -1]
    return splitted


def read_all_raw_data():
    rmid_list = get_total_rmid_list()
    #splitted = task_splitter(rmid_list, 4)
    #for each in rmid_list:
    #    raw_reader(each)
    #    print("Finished for " + str(each))
    workers = Pool(processes = 4)
    workers.map(raw_reader, rmid_list)

read_all_raw_data()
