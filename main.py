from base import get_total_rmid_list
from raw_reader import raw_reader

rmid_list = get_total_rmid_list()
for each in rmid_list:
    raw_reader(each)
    print("Finished for " + str(each))
