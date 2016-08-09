import numpy as np
import matplotlib.pyplot as plt
from position import Location
from base import get_total_rmid_list, save_fig


rmid_list = get_total_rmid_list()
dcf_sum = Location.project_loca + "result/light_curve/dcf.txt"
for each in rmid_list:
    try:
        dcf_file = Location.project_loca + "result/light_curve/" + str(each) + \
            "/dcf.dcf"
        dcf_data = np.loadtxt(dcf_file)
        t = dcf_data[:, 0]
        t_m_sig = dcf_data[:, 1]
        t_p_sig = dcf_data[:, 2]
        dcf = dcf_data[:, 3]
        dcf_m_err = dcf_data[:, 4]
        dcf_p_err = dcf_data[:, 5]
        fig = plt.figure()
        plt.errorbar(t, dcf, yerr=[dcf_m_err, dcf_p_err],
                     xerr=[t_m_sig, t_p_sig])
        save_fig(fig, Location.project_loca + "result/light_curve/" + str(each),
                 "dcf")
        plt.close()
        max_index = dcf.argmax()
        t_max = t[max_index]
        t_max_m_sig = t_m_sig[max_index]
        t_max_p_sig = t_p_sig[max_index]
        sum_file = open(dcf_sum, "a")
        sum_file.write(str(each) + " " + str(t_max) + " " + str(t_max_m_sig) +
                       " " + str(t_max_p_sig) + "\n")
        sum_file.close()
    except Exception as reason:
        print(str(each) + " failed due to " + str(reason))
