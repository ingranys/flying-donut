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
from utils.render import points, vectors, colors, animate3d

R1 = 1
R2 = 2

n_theta = 50
n_phi = 500

size = 12
n_points = n_phi*n_theta
spotlight = np.array([-1,2,7])
char = [" ", ". ", ": ", "; ", "= ", "! ", "* ", "# ", "$ ", "@ "]
char = [" ", ". ", ": ", "; ", "+ ", "? ", "% ", "S ", "# ", "@ "]


X,Y,Z = base()
M_donut,V_normals = donut(R1*X,R2*X,Z,n_theta,Y,n_phi)
#points(M_donut,-90,135)
#vectors(M_donut,V_normals,-90,135,5)

M_rotated_donut = rotate(M_donut, rotations(X,1,Z,1))
V_rotated_normals = rotate(V_normals, rotations(X,1,Z,1))
#points(M_rotated_donut,-90,135)
#vectors(M_rotated_donut,V_rotated_normals,-90,135,5)
#animate3d(M_rotated_donut,rotations(X,(2*np.pi)*7/100,Y,(2*np.pi)*3/100),rotate,5,50,-90,100,5)

#initial_shades = shades(M_donut,V_normals,spotlight)
rotated_shades = shades(M_rotated_donut,V_rotated_normals,spotlight)
#colors(M_donut,initial_shades,-90,135,10)
#colors(M_rotated_donut,rotated_shades,-90,135,10)

scr = curses.initscr()
scr.clear()
scr.refresh()

rotations = rotations(X,(2*np.pi)*7/100,Y,(2*np.pi)*3/100)
for k in range(99):
    M_rotated_donut = rotate(M_rotated_donut, rotations)
    V_rotated_normals = rotate(V_rotated_normals, rotations)
    rotated_shades = shades(M_rotated_donut,V_rotated_normals,spotlight)

    M_pixels = np.zeros((2*size,2*size))
    M_resized_donut = (size+np.floor((2*size/7)*M_rotated_donut[:,:2])).astype('int')
    for i in range(n_points):
        x, y = M_resized_donut[i]
        M_pixels[y,x] = np.maximum(rotated_shades[i],M_pixels[y,x])
    M_ascii_pixels = [[char[int(np.floor(10*M_pixels[i,j]))] for i in range(2*size)] for j in range(2*size)]

    scr.addstr(0, 0, str(k) )
    for i in range(2*size):
        for j in range(2*size):
            scr.addstr(i, 2*j, M_ascii_pixels[i][j])
    scr.addstr(0, 0, str(k) )
    scr.refresh()
scr.clear()
scr.refresh()


"""
if __name__ == '__main__':
    main()
"""