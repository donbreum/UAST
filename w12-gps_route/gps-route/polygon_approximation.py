#!/usr/bin/python3
"""
Main project executable.
"""
# Standard libraries
import math
import numpy as np
import skimage.measure
# Third party libraries
import visvalingamwyatt as vw
import plotter
# Local libraries

def minimize_distance(points, threshold=0.2):
    bool_tmp = [True]*len(points)
    it = 0 # number in the list currently being inspected from

    for x in range(len(points)-2):
        skip = 0
        while True:
            if (x+2+skip+it) < (len(points)-2):
                x0, y0 = points[x+it][0], points[x+it][1]
                x1, y1 = points[x+1+it][0], points[x+1+it][1]
                x2, y2 = points[x+2+skip+it][0], points[x+2+skip+it][1]
                dist = point_line_distance(x0,y0,x1,y1,x2,y2)
            else:
                break
            if dist > threshold:
                break
            else:
                bool_tmp[x+1+it] = False
                skip += 1
                it += 1
    new_wp = points[bool_tmp]
    print ("Number of wp",len(new_wp))
    # import pdb; pdb.set_trace()
    return new_wp

def wyatt(points, number_of_wp):
    simplifier = vw.Simplifier(points[:,3:].astype(np.float))
    simplified_path = simplifier.simplify(number_of_wp)

    return simplified_path

def point_line_distance(x0,y0,x1,y1,x2,y2):
    return abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1)) / math.sqrt((x2-x1)*(x2-x1)
                                                            + (y2-y1)*(y2-y1))

def point_point_distance(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    return math.sqrt(dx*dx+dy*dy)


def skimage_rdp(points, tolerance=3):
    """
    Ramer-Douglas-Peucker algorithm.
    """
    vertices = skimage.measure.approximate_polygon(points, tolerance)
    return vertices


def simplify_reumann_witkam(tolerance, p, step=-1):
    """
    Reumann Witkam algorithm

    Code extracted from:
    https://github.com/keszegrobert/polyline-simplification/blob/master/
    4.%20Reumann-Witkam.ipynb
    """
    mask = np.ones(len(p),dtype='bool')
    first = 0
    second = 1
    third = 2

    marker = np.array([p[first],p[second],p[third]],dtype='double')

    if step == -1:
        maxstep = len(p)
    else:
        maxstep = min(step,len(p))

    for i in range(0,min(maxstep,len(p)-2)):

        dist = point_line_distance(p[third,0],p[third,1],p[first,0],p[first,1],
                                   p[second,0],p[second,1])
        #print dist
        if dist <= tolerance:
            mask[third] = False
            third = third+1
        else:
            first = second
            second = third
            third = third+1
        marker = np.array([p[first],p[second]],dtype='double')

    return mask,marker


def simplify_opheim(tolerance,maxdist,p,step=-1):
    mask = np.ones(len(p),dtype='bool')
    marker = np.array([],dtype='double')
    first = 0
    second = 1
    third = 2

    marker = np.array([p[first],p[second]],dtype='double')

    if step == -1:
        maxstep = len(p)
    else:
        maxstep = min(step,len(p))

    for i in range(0,min(step,len(p)-2)):
        ldist = point_line_distance(p[third,0],p[third,1],p[first,0],p[first,1],p[second,0],p[second,1])
        pdist = point_point_distance(p[third,0],p[third,1],p[first,0],p[first,1])
        if ldist <= tolerance and pdist < maxdist:
            mask[second] = False
            second = third
            third = third+1
        else:
            first = second
            second = third
            third = third+1
    marker = np.array([p[first],p[second]],dtype='double')
    return mask,marker

def simplify_lang(tolerance,p,step):
    mask = np.ones(len(p),dtype='bool')
    start = 0
    end = 2

    marker = np.array([p[start],p[end]],dtype='double')

    if step == -1:
        maxstep = len(p)
    else:
        maxstep = min(step,len(p))

    while end < len(p) and end < maxstep:
        bGreater = False
        for i in range(start,end):
            ldist = point_line_distance(p[i,0],p[i,1],
                                        p[start,0],p[start,1],
                                        p[end,0],p[end,1])
            if ldist>tolerance:
                bGreater = True
                break
        marker = np.array([p[start],p[end]])
        if bGreater:
            mask[start+1:end-1] = False
            start = end-1
            end = start+2
        else:
            end = end+1
    mask[start+1:end-1]=False


    return mask,marker
