#!/usr/bin/python3
"""
Main project executable.
"""
# Standard libraries
import matplotlib.pyplot as plt
import numpy as np
# Third party libraries
# Local libraries
from utm import utmconv
import plotter
import polygon_approximation
# from pyvisvalingamwhyatt.polysimplify import VWSimplifier
import remove_outliers
from hermite import cubic_hermite_spline
from pylab import *

def parse_data(inputfile="./resources/position.log"):
    """
    Read the specified file and return an array with the parsed data.

    The file is assumed to contain data separated by commas. Only the
    lines containing 9 elements will be taken into consideration.
    Moreover, the lines beginning with '#' will be ignored.
    """
    gps_data = np.array
    with open(inputfile, 'r') as data_file:
        for line in data_file:
            row_data = line.rstrip().split(',')
            # Read only the lines with 4 items.
            if len(row_data) == 4:
                # The first time, the exception is raised and the array
                # is initialized.
                try:
                    gps_data = np.vstack((gps_data, row_data))
                except ValueError:
                    gps_data = np.array(row_data)
    # Transform the string-type data to float.
    gps_data = gps_data.astype(np.float)
    return gps_data


def main():
    gps_data = parse_data()
    times = gps_data[:, 0].reshape((-1, 1))
    geo_coordinates = gps_data[:, 1:3]
    utm_values = np.array
    uc = utmconv()
    for point in geo_coordinates:
        new_utm_values = uc.geodetic_to_utm(point[0], point[1])
        # The first time, the exception is raised and the array is initialized.
        try:
            utm_values = np.vstack((utm_values, new_utm_values))
        except ValueError:
            utm_values = new_utm_values
    utm_coordinates = utm_values[:, 3:].astype(np.float)
    vertices = polygon_approximation.skimage_rdp(utm_coordinates)
    mask, marker = polygon_approximation.simplify_lang(10, utm_coordinates,
                                                       step=100)
    simplified = utm_coordinates[mask]

    #deleted points
    # deleted = utm_coordinates[np.logical_not(mask)]
    # plt.scatter(deleted[:,0],deleted[:,1],color='red',marker='x',s=50,linewidth=2.0)
    # plt.plot(rw_simplified[:,0],rw_simplified[:,1])
    # plt.show()
    # plotter.path_plot(utm_coordinates, rw_simplified)
    #plotter.path_plot(utm_coordinates, vertices)
    utm_data = np.hstack((utm_values, times))
    # ex 4.3
    utm_data = remove_outliers.remove_outliers(utm_data,15,
                                              plot_data=False)

    # ex. 4.5 - convert back to geo

    geodetic_values = np.array
    for point in utm_data:
        new_geodetic_values = uc.utm_to_geodetic(str(utm_data[:,0][0]),
                                                 int(utm_data[:,1][0]),
                                                 float(utm_data[:,3][0]),
                                                 float(utm_data[:,4][0]))
        # The first time, the exception is raised and the array is initialized.
        try:
            geodetic_values = np.vstack((geodetic_values, new_geodetic_values))
        except ValueError:
            geodetic_values = new_geodetic_values

    # ex 4.7 - fixed wing path cubic hermite spline
    utm_coordinates = utm_data[:,3:5].astype(np.float)
    vertices = polygon_approximation.skimage_rdp(utm_coordinates)
    #plotter.path_plot(utm_coordinates, vertices)
    #import pdb; pdb.set_trace()
    chs = cubic_hermite_spline();
    splines = chs.get_path(vertices)

    plotter.path_plot(vertices, splines)

    return utm_coordinates

if __name__ == "__main__":
    gps_data = main()
