#!/usr/bin/python3
"""
Main project executable.
"""
# Standard libraries
import skimage.measure
# Third party libraries
# Local libraries


def skimage_rdp(points, tolerance=3):
    """
    Ramer-Douglas-Peucker algorithm.
    """
    vertices = skimage.measure.approximate_polygon(points, tolerance)
    return vertices
