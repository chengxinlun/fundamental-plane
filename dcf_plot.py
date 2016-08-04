import numpy as np
import matplotlib.pyplot as plt
from position import Location
from base import get_total_rmid_list, save_fig


rmid_list = get_total_rmid_list()
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
        plt.errorbar(t, dcf, yerr=[dcf_m_err, dcf_p_err], xerr=[t_m_sig, t_p_sig])
        save_fig(fig, Location.project_loca + "result/light_curve/" + str(each),
                 "dcf")
        plt.close()
    except Exception as reason:
        print(str(each) + " failed due to " + str(reason))
