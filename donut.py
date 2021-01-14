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


from utils.geom import base, donut, rotations, rotate, projection, shades, pixels
from utils.render import points, vectors, colors, image, animate3d
from utils.console import warning, screen, reset, asciis, render


# USER INPUTS
X,Y,Z = base()
R1 = 1
radius_ratio = 2
n_theta = 30 #80
n_phi = 100 #200

axis_A = X
axis_B = Z
start_angle_A = 0.5
start_angle_B = -0.5

spotlight = [0,2,10]

n_pixels = 40   # -1 is for autoscale
zoom = 1.0

n_frames = 500
speed = 1.0
speed_ratio = 3/7 # B/A, nice examples : 3/7, 3/1, ...

preview = True
debug = False

char = [" ", ".", ",", "-", "~", ":", ";", "=", "!", "*", "#", "$", "@"]
#char = [".", ",", "-", "~", ":", ";", "=", "+", "!", "?", "*", "&", "$", "%", "#", "@ "]


# DYNAMIC VARIABLES
R2 = radius_ratio*R1
donut_size = 2*(R1+R2)
n_points = n_phi*n_theta
speed = speed/5

# STATIC VARIABLES
azimut = -90
elevation = 135
warning_treshold = 1000
preview_waiting = 5
debug_waiting = 10


M_donut,V_normals, M_circles = donut(R1,R2,X,Z,n_theta,Y,n_phi)

initial_rotations =  rotations(axis_A,start_angle_A,axis_B,start_angle_B)
M_rotated_donut = rotate(M_donut,initial_rotations)
V_rotated_normals = rotate(V_normals, initial_rotations)

rotations = rotations(axis_A,speed,axis_B,speed_ratio*speed)

if debug :
    if n_points>warning_treshold:
        warning('Debug',debug_waiting)
    points(M_circles,azimut,elevation,donut_size,
                'base circles (centered and translated)')
    points(M_donut,azimut,elevation,donut_size,
                'donut surface points')
    vectors(M_donut,V_normals,azimut,elevation,donut_size,
                'donut surface normals')
    points(M_rotated_donut,azimut,elevation,donut_size,
                'donut surface points (inital position)')
    vectors(M_rotated_donut,V_rotated_normals,azimut,elevation,donut_size,
                'donut surface normals (initial position)')

if preview:  
    if n_points>warning_treshold:
        warning('Preview',preview_waiting) 
    initial_shades, _ = shades(M_donut,V_normals,spotlight)
    rotated_shades, _ = shades(M_rotated_donut,V_rotated_normals,spotlight)
    colors(M_donut,initial_shades,azimut,elevation,donut_size,
                'donut illumination')
    colors(M_rotated_donut,rotated_shades,azimut,elevation,donut_size,
                'donut illumination (initial position)')
    animate3d(M_rotated_donut,rotations,rotate,n_frames,azimut,elevation,donut_size,
                'donut movement')

scr,frame_height,frame_width = screen(n_pixels)

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