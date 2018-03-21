#!/usr/bin/python3
"""
Main project executable.
"""
# Standard libraries
import matplotlib.pyplot as plt
import os
# Third party libraries
# Local libraries


def format_plotting():
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['font.size'] = 22
    #    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.2 * plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = 0.9 * plt.rcParams['font.size']
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


def path_plot(path_1, path_2=None):
    """Draw on a figure the desired and real paths."""
    x1, y1 = path_1[:,0], path_1[:,1]
    # If there is only one point in the array, an IndexError will be raised.
    try:
        x2, y2 = path_2[:,0], path_2[:,1]
    except IndexError:
        x2, y2 = path_2[0], path_2[1]
    # Draws the figure
    format_plotting()
    ax = plt.subplot(111)
    # Plotting of the 2 lines, with 'point' markers and blue and red colours
    ax.plot(x1, y1, 'b.-', label="real path")
    try:
        ax.plot(x2, y2, 'r.-', label="approximated path")
    except:
        pass
    ax.grid()
    ax.legend()
    plt.title("GPS real and corrected path")
    ax.axis('equal')
    # ax.set_xlim([-2000, 2000])
    # ax.set_ylim([-2000, 2000])
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    script_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig('{}/tmp/path_plot.eps'.format(script_path), bbox_inches='tight')
    plt.show()
    return
