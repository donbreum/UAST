#!/usr/bin/python3

import numpy as np
from utm import utmconv

def utm_to_geodetic(utm_data):
    uc = utmconv()
    geodetic_coordinates = np.array
    for point in utm_data:
        # import pdb; pdb.set_trace()
        new_geodetic_coordinates = uc.utm_to_geodetic(str(point[0]),
                                                     int(point[1]),
                                                     float(point[3]),
                                                     float(point[4]))

        # The first time, the exception is raised and the array is initialized.
        try:
            geodetic_coordinates = np.vstack((geodetic_coordinates,
                                              new_geodetic_coordinates))

        except ValueError:
            geodetic_coordinates = new_geodetic_coordinates

    return geodetic_coordinates

def geodetic_to_utm(geo_coordinates):
    utm_values = np.array
    uc = utmconv()
    for point in geo_coordinates:
        new_utm_values = uc.geodetic_to_utm(point[0], point[1])
        # The first time, the exception is raised and the array is initialized.
        try:
            utm_values = np.vstack((utm_values, new_utm_values))
        except ValueError:
            utm_values = new_utm_values
    return utm_values
