#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

# max speed is set to 15 m/s (54 km/h).
# normal max speed for common drones
def remove_outliers(utm_c, max_speed=15., plot_data=False):

    utm_c2 = np.vstack((utm_c[0, :], utm_c))
    diff = utm_c - utm_c2[:-1]
    speed = np.hypot(diff[:, 1], diff[:, 2]) / diff[:,0]
    new_utm = utm_c[speed < max_speed]
    #import pdb; pdb.set_trace()

    if plot_data:
        fig = plt.figure()
        plt.hold(True)
        plt.xlabel("UTM N", fontsize=20)
        plt.ylabel("UTM E", fontsize=20)
        plt.title("Result after removing outliers", fontsize=23)

        plt.plot(utm_c[:,1], utm_c[:,2], color="blue",
                 linewidth=1.5, linestyle=":", label='Original data')
        plt.plot(new_utm[:,1], new_utm[:,2], color="red", linewidth=1.5,
                 label='Outlier filtered data')
        plt.legend(loc=0)
        #plt.show()
        fig.savefig("resources/result_removing_outliers.png")
        #plt.close()
    return new_utm[:,1:3]
