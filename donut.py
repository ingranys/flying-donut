#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Countdown Numbers Game solver.

For more information, see README.

For usage, use help menu <python3 donut.py -h>.

Project can be found here <https://github.com/ingranys/flying-donut>.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "ingranys"
__contact__ = "ingranys@protonmail.com"
__copyright__ = "Copyright 2021, Mustapha Gaies, Toulouse (France)"
__date__ = "2021/01/09"
__deprecated__ = False
__email__ =  "ingranys@protonmail.com"
__license__ = "GPLv3"
__maintainer__ = None
__status__ = "Production"
__version__ = "0.1.0"


import curses
import numpy as np

from utils.geom import base, donut, rotations, rotate, projection, shades, pixels
from utils.render import points, vectors, colors, image, animate3d
from utils.console import warning, screen, reset, asciis, render


# USER INPUTS
X,Y,Z = base()
R1 = 1
radius_ratio = 2
n_theta = 100 #80
n_phi = 300 #200

axis_A = X
axis_B = Z
start_angle_A = 0.5
start_angle_B = -0.5

spotlight = [0,2,10]

n_pixels = 25
zoom = 1.0

n_frames = 500
speed = 1.0
speed_ratio = 3/7 # B/A, 3/7-3/1 gives nice results

preview = False
debug = False

char = [" ", ".", ",", ";" "+", "=", "&", "$", "#", "@"]
#char = [".", ",", "-", ":", "+", "!", "?", "S", "$", "#"]
#char = [".", ",", "-", "~", ":", ";", "=", "+", "!", "?", "*", "$", "%", "#", "@ "]



# INDUCED PARAMETERS
R2 = radius_ratio*R1
donut_size = 2*(R1+R2)
distance = donut_size/zoom
n_points = n_phi*n_theta
frame_height = n_pixels
frame_width = 2*n_pixels
speed = speed/5


M_donut,V_normals, M_cirlces = donut(R1*X,R2*X,Z,n_theta,Y,n_phi)

M_rotated_donut = rotate(M_donut, rotations(axis_A,start_angle_A,axis_B,start_angle_B))
V_rotated_normals = rotate(V_normals, rotations(axis_A,start_angle_A,axis_B,start_angle_B))

rotations = rotations(axis_A,speed,axis_B,speed_ratio*speed)

if debug :
    if n_points>1000:
        warning('Debug',10)
    points(M_cirlces,-90,135,donut_size)
    points(M_donut,-90,135,donut_size)
    vectors(M_donut,V_normals,-90,135,donut_size)
    points(M_rotated_donut,-90,135,donut_size)
    vectors(M_rotated_donut,V_rotated_normals,-90,135,donut_size)

if preview:  
    if n_points>1000:
        warning('Preview',5) 
    initial_shades, _ = shades(M_donut,V_normals,spotlight)
    rotated_shades, _ = shades(M_rotated_donut,V_rotated_normals,spotlight)
    colors(M_donut,initial_shades,-90,135,donut_size)
    colors(M_rotated_donut,rotated_shades,-90,135,donut_size)
    animate3d(M_rotated_donut,rotations,rotate,n_frames,-90,135,donut_size)

scr = screen()

try:
    for k in range(n_frames):
        M_rotated_donut = rotate(M_rotated_donut, rotations)
        V_rotated_normals = rotate(V_rotated_normals, rotations)
        rotated_shades, light_indexes = shades(M_rotated_donut,V_rotated_normals,spotlight)

        M_pixels = pixels(M_rotated_donut,rotated_shades,light_indexes,
                            frame_height,frame_width,donut_size,zoom)
        
        M_asciis = asciis(M_pixels,char)

        render(M_asciis,scr,k,n_frames)

        if debug:
            image(M_pixels)
    
    reset()
except KeyboardInterrupt:
    reset()
    print('Rendering has been interrupted.')
except Exception as e:
    reset()
    raise(e)


"""
if __name__ == '__main__':
    main()
"""