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


import time
import curses
import numpy as np

from utils.geom import base, donut, rotations, rotate, projection,shades
from utils.render import points, vectors, colors, image, animate3d


# USER INPUTS
X,Y,Z = base()
R1 = 1
R2 = 2
n_theta = 80 #80
n_phi = 200 #200

axis_A = X
axis_B = Z
start_angle_A = 0.5
start_angle_B = -0.5

spotlight = [1,1,8]

n_pixels = 25
zoom = 1.0

n_frames = 100
speed = 1.0
speed_ratio = 3/7 # B/A, 3/7-3/1 gives nice results

preview = False
debug = False

char = [" ", ", ", "~  ", "; ", "= ", "! ", "* ", "$ ", "# ", "@ "]
#char = [". ", ", ", "- ", ": ", "+ ", "! ", "? ", "S ", "$ ", "# "]


# INDUCED PARAMETERS
donut_size = 2*(R1+R2)
n_points = n_phi*n_theta
frame_height = n_pixels
frame_width = 2*n_pixels
speed = speed/5


M_donut,V_normals, M_cirlces = donut(R1*X,R2*X,Z,n_theta,Y,n_phi)

M_rotated_donut = rotate(M_donut, rotations(axis_A,start_angle_A,axis_B,start_angle_B))
V_rotated_normals = rotate(V_normals, rotations(axis_A,start_angle_A,axis_B,start_angle_B))

rotations = rotations(axis_A,speed,axis_B,speed_ratio*speed)


if preview:   
    initial_shades, _ = shades(M_donut,V_normals,spotlight)
    rotated_shades, _ = shades(M_rotated_donut,V_rotated_normals,spotlight)
    colors(M_donut,initial_shades,-90,135,10)
    colors(M_rotated_donut,rotated_shades,-90,135,10)
    animate3d(M_rotated_donut,rotations,rotate,5,10,-90,135,10)

if debug :
    points(M_cirlces,-90,135,10)
    points(M_donut,-90,135,10)
    vectors(M_donut,V_normals,-90,135,5)
    points(M_rotated_donut,-90,135,10)
    vectors(M_rotated_donut,V_rotated_normals,-90,135,5)


scr = curses.initscr()
scr.clear()
scr.refresh()

try:
    for k in range(n_frames):
        M_rotated_donut = rotate(M_rotated_donut, rotations)
        V_rotated_normals = rotate(V_rotated_normals, rotations)
        rotated_shades, light_indexes = shades(M_rotated_donut,V_rotated_normals,spotlight)

        M_pixels = np.zeros((frame_height,frame_width))
        x_donut = (np.floor(
                    (frame_width/2)+
                    (zoom*frame_width/donut_size)*M_rotated_donut[:,0])).astype('int')
        y_donut = (np.floor(
                    (frame_height/2)-
                    (zoom*frame_height/donut_size)*M_rotated_donut[:,1])).astype('int')
        x_indexes = np.where(np.logical_or( x_donut<0 , x_donut >= frame_width) )[0]
        y_indexes = np.where(np.logical_or( y_donut<0 , y_donut >= frame_height)  )[0]
        
        valid_index = np.setdiff1d(light_indexes,np.concatenate([x_indexes,y_indexes]))
        for idx in valid_index:
            x = x_donut[idx]
            y = y_donut[idx]
            M_pixels[y,x] = np.maximum(rotated_shades[idx],M_pixels[y,x])
        M_ascii_pixels = [[char[int(np.floor(10*M_pixels[i,j]))] for j in range(frame_width)] for i in range(frame_height)]

        scr.addstr(0, 0, str(k) )
        for i in range(frame_height):
            for j in range(frame_width):
                scr.addstr(i, j, M_ascii_pixels[i][j])
        msg = '{0}/{1}'.format(k+1,n_frames)
        scr.addstr(0, 0, msg )
        scr.refresh()

        if debug:
            image(M_pixels)
    
    curses.endwin()

except KeyboardInterrupt:
    curses.endwin()
    print('Rendering has been interrupted.')
except Exception as e:
    curses.endwin()
    raise(e)


"""
if __name__ == '__main__':
    main()
"""