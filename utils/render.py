#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 3D and 2D rendering module for flying donut.

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
__date__ = "2021/01/16"
__deprecated__ = False
__email__ =  "ingranys@protonmail.com"
__license__ = "GPLv3"
__maintainer__ = None
__status__ = "Production"
__version__ = "0.1.0"


import warnings
# Ignore MatplotlibDeprecationWarning while importing matplotlib.animation
warnings.filterwarnings("ignore",category=UserWarning)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def points(M,azimut=None,elevation=None,size=10,title='points'):
    """Plot points in 3D. 

    Args:
        M (array([float]): Set of points (must be shape (n,3)).
        azimut (float, optional): Azimuth angle for camera position (angle between x and p). Defaults to None.
        elevation (float, optional): Elevation angle for camera position (angle between p and r). Defaults to None.
        size (int, optional): Expected size of the object. Defaults to 10.
        title (str, optional): Title for the figure window. Defaults to 'points'.
    """
    fig = plt.figure(title.upper())
    ax = fig.add_subplot(projection='3d')
    ax.scatter(M[:,0],M[:,1],M[:,2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    axis_range = [-(1+np.floor(size/2)),1+np.floor(size/2)]
    ax.set_xlim(axis_range)
    ax.set_ylim(axis_range)
    ax.set_zlim(axis_range)
    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation

    plt.show()


def vectors(M,V,azimut=None,elevation=None,size=10,length=None,title='vectors'):
    """Plot vectors in 3D.

    Args:
        M (array([float]): Set of vector locations (must be shape (n,3)).
        V ([type]): Set of vectors (must be shape (n,3)).
        azimut (float, optional): Azimuth angle for camera position (angle between x and p). Defaults to None.
        elevation (float, optional): Elevation angle for camera position (angle between p and r). Defaults to None.
        size (int, optional): Expected size of the object. Defaults to 10.
        length ([type], optional): Length of the arrows. Defaults to None.
        title (str, optional): Title for the figure window. Defaults to 'vectors'.
    """
    fig = plt.figure(title.upper())
    ax = fig.add_subplot(projection='3d')
    ax.quiver(M[:,0],M[:,1],M[:,2],V[:,0],V[:,1],V[:,2])
    ax.set_xlabel('X')
    ax.set_ylabel('Yl')
    ax.set_zlabel('Z')
    axis_range = [-(1+np.floor(size/2)),1+np.floor(size/2)]
    ax.set_xlim(axis_range)
    ax.set_ylim(axis_range)
    ax.set_zlim(axis_range)
    if length:
        ax.length = length
    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation

    plt.show()


def colors(M,colors,azimut=None,elevation=None,size=10,title='colors'):
    """Plot points in 3D with colors.
    Illumination intensities (grayscale) are automatically shifted to colors.

    Args:
        M (array([float]): Set of points (must be shape (n,3)).
        colors (array[float]): Point colors (must be shape (n,)).
        azimut (float, optional): Azimuth angle for camera position (angle between x and p). Defaults to None.
        elevation (float, optional): Elevation angle for camera position (angle between p and r). Defaults to None.
        size (int, optional): Expected size of the object. Defaults to 10.
        title (str, optional): Title for the figure window. Defaults to 'colors'.
    """
    fig = plt.figure(title.upper())
    ax = fig.add_subplot(projection='3d')
    ax.scatter(M[:,0],M[:,1],M[:,2],c=colors)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    axis_range = [-(1+np.floor(size/2)),1+np.floor(size/2)]
    ax.set_xlim(axis_range)
    ax.set_ylim(axis_range)
    ax.set_zlim(axis_range)
    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation

    plt.show()


def image(pixels):
    """Display 2D grayscale image and change aspect ratio from 2:1 to 1:1.

    Args:
        pixels (array[float]): Pixel values (must shape (x,y)).
    """
    y, x = pixels.shape
    plt.imshow(pixels,interpolation='none',cmap='gray',extent=[0,x,0,y],aspect=2)

    plt.show()


def update3d(i, rotations, function, scat):
    """Update scene based on given rotations.

    Args:
        i (int): Iteration number. Not used.
        rotations (array[rotation]): 3D rotations to be applied (must contain 1 more rotations).
        function (function): Input function implementing rotation.
        scat (array[float]): Scene information containing points in 3D.

    Returns:
        scat (array[float]): Updated scene.
    """
    donut = np.array(scat._offsets3d).T
    rotated_donut = function(donut,rotations)
    scat._offsets3d = (rotated_donut[:,0],rotated_donut[:,1],rotated_donut[:,2])

    return scat


def animate3d(donut,rotations,function,n_frames,azimut=None,elevation=None,size=10,title='animation'):
    """Play 3D animation of the object moving according to rotations.

    Args:
        donut (array[float]): Set of points representing the object in 3D (shape must be (n,3))
        rotations (array[rotation]): 3D rotations to be applied (must contain 1 more rotations).
        function (function): Input function implementing rotation.
        n_frames (int): Number of frames.
        azimut (float, optional): Azimuth angle for camera position (angle between x and p). Defaults to None.
        elevation (float, optional): Elevation angle for camera position (angle between p and r). Defaults to None.
        size (int, optional): Expected size of the object. Defaults to 10.
        title (str, optional): Title for the figure window. Defaults to 'animation'.
    """
    fig = plt.figure(title.upper())
    ax = fig.gca(projection='3d')
    scat = ax.scatter(donut[:,0], donut[:,1], donut[:,2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')   
    axis_range = [-(1+np.floor(size/2)),1+np.floor(size/2)]
    ax.set_xlim(axis_range)
    ax.set_ylim(axis_range)
    ax.set_zlim(axis_range)

    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation
        
    ani = animation.FuncAnimation(fig, update3d, frames=n_frames, 
                                        fargs=(rotations,function,scat))
    ani.repeat = True

    plt.show()