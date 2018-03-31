#!/usr/bin/python3
import numpy as np
import plotter
import matplotlib.pyplot as plt

class remove_outliers():
    def __init__(self):
        pass
# max speed is set to 15 m/s (54 km/h).
# normal max speed for common drones
    def remove_outliers(self, utm_data, max_speed=15., plot_data=False):

        utm_data_temp = utm_data[:,3:6].astype(np.float)
        utm_c2 = np.vstack((utm_data_temp[0, :], utm_data_temp))
        diff = utm_data_temp - utm_c2[:-1]

        speed = np.hypot(diff[:, 0], diff[:, 1]) / diff[:,2]
        utm_data = utm_data[speed < max_speed]

        # import pdb; pdb.set_trace()
        if plot_data:
            utm = utm_data_temp[speed < max_speed]
            # fig = plt.figure()
            # plt.hold(True)
            # plt.xlabel("UTM N", fontsize=20)
            # plt.ylabel("UTM E", fontsize=20)
            # plt.title("Result after removing outliers", fontsize=23)
            #
            # plt.plot(utm_data_temp[:,0], utm_data_temp[:,1], color="blue",
            #          linewidth=1.5, linestyle=":", label='Original data')
            # plt.plot(utm[:,0], utm[:,1], color="red", linewidth=1.5,
            #          label='Outlier filtered data')
            # plt.legend(loc=0)
            #plt.show()
            plotter.path_plot(utm_data_temp[:,0:2], utm[:,0:2])
            #fig.savefig("resources/result_removing_outliers.png")
            #plt.close()
        return utm_data[:,0:5]
