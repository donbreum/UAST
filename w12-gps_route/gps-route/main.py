#!/usr/bin/python3
"""
Main project executable.
"""
# Standard libraries
import numpy as np
# Third party libraries
# Local libraries
from utm import utmconv
import plotter


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
    plotter.path_plot(utm_coordinates)
    return utm_coordinates


if __name__ == "__main__":
    gps_data = main()
