#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:20:04 2020

@author: jgarciamejia

Library of functions to be used with plot_baffles.py
"""


### MUST ANNOTATE THESE FUNCTIONS!! 

import numpy as np 

# Generate a line from two points 
def define_line_from_pts(x1,x2,y1,y2):
    m =  (y2 - y1) / (x2 - x1)
    b = y1 - (m*x1)
    return (m,b)

# Find line intercept of two lines
# to do : add error in case lines do not intercept! 
def find_line_intercept(m1, b1, m2, b2):
    x = (b2 - b1) / (m1 - m2)
    y = (m1*x) + b1
    #print ('x,y = '+str(x)+','+str(y))
    return (x,y)


# COMMENT ON ASSUMPTIONS. FOR sphere: megative because lenses all toward 
# the +z side and all sides concave from 0 to +z, also all radii of curvature 
# are positive according to zemax convention so no need to consider that separately
# vertex z is the z_coord of the vertex of the surface, assuming z=0 is at the
# primary vertex. So the whole point is that it is all about staying consistent with Zemax.
#Generates x&y arrays to plot a 2D projection of a surface of a lens
# also, incorporate hyperbola and parabola here! 

def xzs_surface_generator(diameter, vertex_z, radius_curv, conic):
    x_array = np.arange(-diameter/2, diameter/2+1, 1)
    if conic == 'sphere':
        z_array = - np.sqrt((radius_curv)**2 - (x_array)**2) + radius_curv + vertex_z
    elif conic == 'plane':
        z_array = vertex_z*np.ones(len(x_array))
    return x_array, z_array

