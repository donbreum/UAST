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

#from visvalingamwyatt.polysimplify import VWSimplifier
from hermite import cubic_hermite_spline
from polygon_approximation import simplify_polygons
from outliers import remove_outliers
from pylab import *

import utm_geo_convert

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


def main(plots=False):
    gps_data = parse_data()
    times = gps_data[:, 0].reshape((-1, 1))
    geo_coordinates = gps_data[:, 1:3]
    utm_values = utm_geo_convert.geodetic_to_utm(geo_coordinates)
    utm_coordinates = utm_values[:, 3:].astype(np.float)
    sp = simplify_polygons()
    vertices = sp.skimage_rdp(utm_coordinates)
    mask, marker = sp.simplify_lang(10, utm_coordinates,
                                                       step=100)
    simplified = utm_coordinates[mask]

    utm_data = np.hstack((utm_values, times))
    # ex 4.3
    ro = remove_outliers()
    filtered_utm_data = ro.remove_outliers(utm_data,15, plot_data=False)
    # ex. 4.4 - simplify path
    filtered_utm_coordinates = filtered_utm_data[:,3:5].astype(np.float)
    vertices = sp.skimage_rdp(filtered_utm_coordinates)
    wyatt = sp.wyatt(utm_values, 10)
    min_dist_path = sp.minimize_distance_and_angle(filtered_utm_coordinates,
                                                   0.2)
    min_dist_path_angle = sp.minimize_distance_and_angle(
        filtered_utm_coordinates, 0.2, True, 45)

    if(plots):
        plotter.path_plot(filtered_utm_coordinates, vertices, wyatt,
                          min_dist_path, min_dist_path_angle)

    # ex. 4.5 - convert back to geo
    filtered_geo_coordinates = utm_geo_convert.utm_to_geodetic(utm_data)


    # ex 4.7 - fixed wing path cubic hermite spline
    if(plots):
        chs = cubic_hermite_spline();
        splines = chs.get_path(vertices)
        plotter.path_plot(vertices, splines)

    # convert vertices to geodetic_coordinates
    left_side = np.zeros((vertices.shape[0],3)).astype(str)
    left_side[:, 0] = "N"
    left_side[:, 1] = 32
    left_side[:, 2] = "U"
    result = np.hstack((left_side, vertices))
    coordinates_for_planner = utm_geo_convert.utm_to_geodetic(result)
    # import pdb; pdb.set_trace()
    # write to file
    new_left_side = np.zeros((vertices.shape[0],1)).astype(str)
    new_result = np.hstack((new_left_side, coordinates_for_planner))
    new_left_side = np.zeros((vertices.shape[0],1)).astype(str)
    new_left_side[:, 0] = "15"
    new_result = np.hstack((new_result, new_left_side))
    np.savetxt("resources/new_log_wps.log", new_result, "%s", ",")

    return utm_coordinates

if __name__ == "__main__":
    gps_data = main(plots=False)
