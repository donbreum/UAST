#!/usr/bin/python3
"""
Module for plotting the 3 first Fresnel zones of different frequencies.
"""
# Standard libraries
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

def format_plotting():
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['font.size'] = 22
    #    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.2 * plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = 0.7 * plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = 0.6 * plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = 0.6 * plt.rcParams['font.size']
    plt.rcParams['savefig.dpi'] = 1000
    plt.rcParams['savefig.format'] = 'eps'
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.loc'] = 'lower right'
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.markersize'] = 3

    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.gca().yaxis.set_ticks_position('left')
    return


def plot_ellipsoids(distance = 100, frequency=1*10**9):
    """NOT WORKING: Need to rearrange x,y,z values to 2-D tuples"""
    fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
    ax = fig.add_subplot(111, projection='3d')
    
    c = 3 * 10**8
    wavelength = c / frequency
    # X coordinates to be plotted, ranging from 0 to the specified distance.
    # The complementary values are calculated as well, for later usage in the
    # Fresnel equation
    d1 = np.linspace(0, distance+1, distance+2)
    d2 = distance - d1
    fresnel_1 = np.sqrt((wavelength*d1*d2) / (d1+d2))

    # Plot:
    ax.plot_surface(d1, fresnel_1, fresnel_1,  rstride=4, cstride=4, color='b')
    plt.show()
    return

def fresnel_2d(distance=100, frequency=1*10**9, out_file="result.eps",
               show=False):
    """
    Plot the first 3 Fresnel zones for the provided frequency in 2-D.

    The zone is callculated for a given communication distance, in
    meters. Moreover, the result is plotted to the specified path with
    eps format.
    """
    c = 3 * 10**8
    wavelength = c / frequency
    # X coordinates to be plotted, ranging from 0 to the specified distance.
    # The complementary values are calculated as well, for later usage in the
    # Fresnel equation
    d1 = np.linspace(0, distance+1, distance+2)
    d2 = distance - d1
    fresnel_1 = np.sqrt((1*wavelength*d1*d2) / (d1+d2))
    fresnel_2 = np.sqrt((2*wavelength*d1*d2) / (d1+d2))
    fresnel_3 = np.sqrt((3*wavelength*d1*d2) / (d1+d2))
    # Set an array with the negative values of the ellipse as well
    x_values = np.hstack((d1,d1))
    y1_values = np.hstack((fresnel_1, -fresnel_1))
    y2_values = np.hstack((fresnel_2, -fresnel_2))
    y3_values = np.hstack((fresnel_3, -fresnel_3))
    # Frequency values formatted for axis name.
    frequency_val = frequency / 10**9
    hz_prefix = "G"
    if frequency_val < 1:
        frequency_val *= 1000
        hz_prefix = "M"
    # Plot values.
    fig = plt.figure()
    plt.plot(x_values, y1_values, label="1st zone")
    plt.plot(x_values, y2_values, label="2nd zone")
    plt.plot(x_values, y3_values, label="3rd zone")
    # Add auxiliary elements to graph.
    plt.xlim(-distance*0.05, distance*1.05)
    plt.ylim(-distance/10, distance/10)
    plt.legend()
    plt.title("Fresnel zones for {}{}Hz frequency".format(frequency_val,
                                                          hz_prefix))
    plt.xlabel('Distance from point A (m)')
    plt.ylabel('Distance from horizontal line (m)')
    plt.grid()
    # Give custom format and show the graph.
    format_plotting()
    script_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig('{}/tmp/{}'.format(script_path, out_file), bbox_inches='tight')
    if show:
        plt.show()
    return


def main():
    fresnel_2d(frequency=2.4*10**9, out_file="fresnel_2.4ghz.eps")
    fresnel_2d(frequency=433*10**6, out_file="fresnel_433mhz.eps")
    fresnel_2d(frequency=5.8*10**9, out_file="fresnel_5.8ghz.eps")
    return


if __name__ == "__main__":
    main()