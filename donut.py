#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Render a rotating donut to the console in ascii.

For more information, see README.

For usage, run <python3 donut.py>.

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
__date__ = "2021/01/14"
__deprecated__ = False
__email__ =  "ingranys@protonmail.com"
__license__ = "GPLv3"
__maintainer__ = None
__status__ = "Production"
__version__ = "0.1.0"


from utils.geom import base, donut, rotations, rotate, projection, shades, pixels
from utils.render import points, vectors, colors, image, animate3d
from utils.console import warning, screen, reset, asciis, render


##########################
###### USER INPUTS #######
##########################
X,Y,Z = base()
R1 = 1
radius_ratio = 2
n_theta = 100
n_phi = 500

axis_A = X
axis_B = Z
start_angle_A = 0.5
start_angle_B = -0.5

spotlight = [0,2,10]

n_pixels = -1   # -1 is for autoscale
zoom = 1.0

n_frames = 500
speed = 0.5
speed_ratio = 3/7 # B/A, nice examples : 3/7, 3/1, ...

preview = False
debug = False

char = [" ", ".", ",", "-", "~", ":", ";", "=", "!", "*", "#", "$", "@"]
#char = [".", ",", "-", "~", ":", ";", "=", "+", "!", "?", "*", "&", "$", "%", "#", "@ "]


##########################
#### DYNAMIC VARIABLES ###
##########################
R2 = radius_ratio*R1
donut_size = 2*(R1+R2)
n_points = n_phi*n_theta


##########################
#### STATIC VARIABLES ####
##########################
azimut = -90
elevation = 135
warning_treshold = 1000
preview_waiting = 5
debug_waiting = 10


def main():
    """
    Main function.
    Key steps are :
    - Generate a 3D representation of the donut surface and normals to surface.
    - Rotate donut to initial position.
    - [Optional] Provide scene rendering for preview and debug mode
    - Frame by frame :
    --- Rotate donut by a small amount.
    --- Project 3D representation of the donut to a 2D screen.
    --- Convert 2D grayscale image to ASCII.
    --- Print ASCII to console.
    --- [Optional] Provide 2D grayscale image for debug mode.
    --- Repeat
    """

    # Generate donut surface based on user inputs
    # (represented by 3D points on the surface and vectors normal to the surface)
    M_donut,V_normals, M_circles = donut(R1,R2,X,Z,n_theta,Y,n_phi)

    # Set the donut to initial position by applying a rotation based on user inputs
    initial_rotations =  rotations(axis_A,start_angle_A,axis_B,start_angle_B)
    M_rotated_donut = rotate(M_donut,initial_rotations)
    V_rotated_normals = rotate(V_normals, initial_rotations)

    # Get the rotations to be apply to the donut between frames based on user inputs
    movement_rotations = rotations(axis_A,speed,axis_B,speed_ratio*speed)

    # Provide useful 3D representations of the scene (points and vectors) for debugging
    if debug :
        # Warning message is printed in case of possible lag
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

    # Provide a preview of the scene (objects, illumination and movement)
    if preview:  
        # Warning message is printed in case of possible lag
        if n_points>warning_treshold:
            warning('Preview',preview_waiting) 
        initial_shades, _ = shades(M_donut,V_normals,spotlight)
        rotated_shades, _ = shades(M_rotated_donut,V_rotated_normals,spotlight)
        colors(M_donut,initial_shades,azimut,elevation,donut_size,
                    'donut illumination')
        colors(M_rotated_donut,rotated_shades,azimut,elevation,donut_size,
                    'donut illumination (initial position)')
        animate3d(M_rotated_donut,movement_rotations,rotate,n_frames,azimut,elevation,donut_size,
                    'donut movement')

    # Initialize the 2D screen (i.e. the console)
    # Rendering is terminated if the constraints can't be applied on screen
    scr,frame_height,frame_width = screen(n_pixels)

    try:
        # Render the scene frame by frame to emulate movement
        for k in range(n_frames):
            
            # Apply rotations to the donut and move it by a little
            M_rotated_donut = rotate(M_rotated_donut, movement_rotations)
            V_rotated_normals = rotate(V_rotated_normals, movement_rotations)
            rotated_shades, light_indexes = shades(M_rotated_donut,V_rotated_normals,spotlight)

            # Give a projection of the donut onto a 2D screen
            M_pixels = pixels(M_rotated_donut,rotated_shades,light_indexes,
                                frame_height,frame_width,donut_size,zoom)
            
            
            # Map grayscale to ascii characters for each pixel
            M_asciis = asciis(M_pixels,char)

            # Print the result to the console
            render(M_asciis,scr,k,n_frames)

            # Provide a 2D grayscale image for comparison when debugging
            if debug:
                image(M_pixels)
        
        reset()
    except KeyboardInterrupt:
        # Keyboard interruption is considered as a legitimate way to stop the animation
        # In this case we stop the rendering and go back to basic console view
        # <ctrl + c >
        reset()
        print('Rendering has been interrupted.')
    except Exception as e:
        # If any other exception than KeyboardInterrutpion is catched
        # We need to reset console to go back to basic console view and then print the error message
        reset()
        raise(e)


if __name__ == '__main__':
    main()