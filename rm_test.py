from rm import rm

rmid = [909]
test = [200, 300, 400]
for each in rmid:
    for each_num in test:
        rm(909, 2 * each_num, each_num, each_num, outname=each_num)
