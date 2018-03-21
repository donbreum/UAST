#!/usr/bin/python3
"""
Main project executable.
"""
# Standard libraries
import numpy as np
# Third party libraries
# Local libraries
from utm import utmconv


def parse_data(inputfile="./resources/position.log"):
    """
    Read the specified file and return an array with the parsed data.

    The file is assumed to contain data separated by commas. Only the
    lines containing 9 elements will be taken into consideration.
    Moreover, the lines beginning with '#' will be ignored.
    """
    init = False
    gps_data = np.zeros(9)
    with open(inputfile, 'r') as data_file:
        for line in data_file:
            row_data = line.rstrip().split(',')
            # Read only the lines with 9 items, and ignore headers as well.
            if len(row_data) == 4  and row_data[0][0] != "#":
                # The first time, the array has to be initialized.
                if not init:
                    gps_data = np.array(row_data)
                    init = True
                else:
                    gps_data = np.vstack((gps_data, row_data))
    # Transform the string-type data to float.
    gps_data = gps_data.astype(np.float64)
    return gps_data


def main():
    gps_data = parse_data()
    geo_coordinates = gps_data[1:3]
    uc = utmconv()
    hemisphere, zone, letter, easting, northing = uc.geodetic_to_utm(test_lat,test_lon)
    return gps_data


if __name__ == "__main__":
    gps_data = main()
