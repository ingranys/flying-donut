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

R1 = 1
R2 = 2

n_theta = 80
n_phi = 200
n_points = n_phi*n_theta

start_angleA = 0.5
start_angleB = -0.5

spotlight = np.array([1,1,8])

size = 16
n_frames = 500
speed = 1/100

preview = False


char = [" ", ". ", ": ", "; ", "= ", "! ", "* ", "# ", "$ ", "@ "]
char = [" ", ", ", "~  ", "; ", "= ", "! ", "* ", "# ", "$ ", "@ "]
#char = [" ", ". ", ": ", "; ", "+ ", "? ", "% ", "S ", "# ", "@ "]

X,Y,Z = base()
M_donut,V_normals, M_cirlces = donut(R1*X,R2*X,Z,n_theta,Y,n_phi)
#points(M_cirlces,-90,135,10)
#points(M_donut,-90,135,10)
#vectors(M_donut,V_normals,-90,135,5)

M_rotated_donut = rotate(M_donut, rotations(X,start_angleA,Z,start_angleB))
V_rotated_normals = rotate(V_normals, rotations(X,start_angleA,Z,start_angleB))
rotations = rotations(X,7*speed,Z,3*speed)
#points(M_rotated_donut,-90,135,10)
#vectors(M_rotated_donut,V_rotated_normals,-90,135,5)
if preview:   
    initial_shades, _ = shades(M_donut,V_normals,spotlight)
    rotated_shades, _ = shades(M_rotated_donut,V_rotated_normals,spotlight)
    colors(M_donut,initial_shades,-90,135,10)
    colors(M_rotated_donut,rotated_shades,-90,135,10)
    animate3d(M_rotated_donut,rotations,rotate,5,10,-90,135,10)


scr = curses.initscr()
scr.clear()
scr.refresh()

#start = time.time()
for k in range(n_frames):
    M_rotated_donut = rotate(M_rotated_donut, rotations)
    V_rotated_normals = rotate(V_rotated_normals, rotations)
    rotated_shades, light_indexes = shades(M_rotated_donut,V_rotated_normals,spotlight)

    M_pixels = np.zeros((2*size,4*size))
    x_donut = (2*size+np.floor((4*size/7)*M_rotated_donut[:,0])).astype('int')
    y_donut = (size-np.floor((2*size/7)*M_rotated_donut[:,1])).astype('int')
    for idx in light_indexes:
        x = x_donut[idx]
        y = y_donut[idx]
        M_pixels[y,x] = np.maximum(rotated_shades[idx],M_pixels[y,x])
    M_ascii_pixels = [[char[int(np.floor(10*M_pixels[i,j]))] for j in range(4*size)] for i in range(2*size)]

    #image(M_pixels)

    scr.addstr(0, 0, str(k) )
    for i in range(2*size):
        for j in range(4*size):
            scr.addstr(i, j, M_ascii_pixels[i][j])
    msg = '{0}/{1}'.format(k+1,n_frames)
    scr.addstr(0, 0, msg )
    scr.refresh()

curses.endwin()
#print("{0} sec".format(time.time()-start))

"""
if __name__ == '__main__':
    main()
"""