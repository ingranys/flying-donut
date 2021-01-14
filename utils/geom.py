#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Custom algebra and trigonometry module for flying donut.

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


import numpy as np
from scipy.spatial.transform import Rotation as R


def base():
    """Compute base vectors [X,Y,Z].

    Returns:
        X,Y,Z : Base vectors.
    """
    X = np.array([1,0,0])
    Y = np.array([0,1,0])
    Z = np.array([0,0,1])

    return X, Y, Z


def donut(R1,R2,V_R,V_theta,n_theta,V_phi,n_phi):
    """Generate a 3D representation of a donut.

    Args:
        R1 (float): Radius of the inner circle.
        R2 (float): Radius of the outer cicle.
        V_R (array[float]): Vector, direction of the radiuses (shape must be (3,)).
        V_theta (array[float]): Vector, rotation axis to generate the inner circle (shape must be (3,)).
        n_theta (int): Number of points along the inner circle.
        V_phi (array[float]): Vector, rotation axis to generate the outer circle (shape must be (3,)).
        n_phi (int): Number of points alont the outer circle.

    Returns:
        M_donut (array[float]) : Points on the surface of the donut (shape is (n_theta*n_phi,3)).
        V_normals (array[float]) : Normal vectors to the surface (shape is (n_theta*n_phi,3)).
        M_circles (array[float]) : Base circle, centered and translated (shape is (2*n_theta,3)).
    """
    # Compute base vectors and total number of points
    V_R1 = R1*V_R
    V_R2 = R2*V_R
    n_points = n_theta*n_phi

    # Generate inner circle by rotating first base vector over first rotation axis
    theta_angles = np.linspace(0,2*np.pi,n_theta,endpoint=False)
    phi_angles = np.linspace(0,2*np.pi,n_phi,endpoint=False)

    # Translate inner circle to final position and keep track of both circles
    M_circle = np.array([R.from_rotvec(theta_angle*V_theta).apply(V_R1) for theta_angle in theta_angles])
    M_translated_circle = M_circle + V_R2
    M_circles = np.vstack((M_circle,M_translated_circle))

    # Generate outer circle by rotating inner circle first over second rotation axis 
    phi_rotations = [R.from_rotvec(phi_angle*V_phi) for phi_angle in phi_angles]
    M_rotated_circles = np.array([phi_rotation.apply(M_translated_circle) for phi_rotation in phi_rotations])
    
    # Get final shape for both arrays
    M_donut = M_rotated_circles.reshape(n_points,3)
    V_normals = np.array([phi_rotation.apply(M_circle) for phi_rotation in phi_rotations]).reshape(n_points,3)

    return M_donut,V_normals,M_circles



def rotations(V_A,angle_A,V_B,angle_B):
    """Generate rotations in 3 dimensions.

    Args:
        V_A (array[float]): Rotation vector for the first rotation (shape must be (3,)).
        angle_A (float): Rotation magnitude in radians for the first rotation.
        V_B (array[float]): Rotation vector for the second rotation (shape must be (3,)).
        angle_B (float): Rotation magnitude in radians for the second rotation.

    Returns:
        rotations (array[rotation]: [first rotation, second rotation].
    """
    R_A = R.from_rotvec(angle_A*V_A)
    R_B = R.from_rotvec(angle_B*V_B)

    return [R_A, R_B]


def rotate(M,rotations):
    """Apply rotations to a set of points or vectors.

    Args:
        M (array[float]): Set of points or vectors (shape must be (n,3)).
        rotations (array[rotation]): 3D rotations to be applied (must contain 1 more rotations).

    Returns:
        M (array[float]): Set of points or vectors after rotations.
    """
    for rotation in rotations:
        M = rotation.apply(M)
    
    return M


def normalize(V):
    """Normalize a set of vectors using L-2 norm : res[i] = V[i]/||V[i]||

    Args:
        V (array[float]): Set of input vectors.

    Returns:
        ||V|| (array[float]): Set of normalized vectors. Same shape as V.
    """
    V_norms =  np.linalg.norm(V, ord=2,axis=1)[:,None]

    return V/V_norms


def projection(V1,V2):
    """Compute dot between two sets of vectors : res[i] = V1[i,:].V2[i,:]. Input arrays must have the same shape.

    Args:
        V1 (array[float]): First set of vectors.
        V2 (array[float]): Second set of vectors.

    Returns:
        sumproduct (array[float]): The results of the dot product row by row. If V1 and V2 shape is (n,m), then sumproduct shape is (n,).
    """
    V1_normalized = normalize(V1)
    V2_normalized = normalize(V2)

    sumproduct =  np.einsum('ij, ij->i', V1_normalized, V2_normalized)

    return sumproduct


def shades(M,N,s):
    """Compute surface illumination at any point on the surface for a given light source position.
    We use a simple Diffuse Lighting Model : I[i] = (Light vector[i]).(Normal vector[i])

    Args:
        M (array[float]): Points on the surface (shape must be (n,3)).
        N (array[float]): Normal vector at each given point on the surface (shape must be (n,3)).
        s (array[float]): Light source position (shape must be (3,)).

    Returns:
        lambert (array[float]): Illumination value at each given point on the surface (shape is (n,)).
        light_indexes (array[float]): Indexes representating the points on the surface with "postive" illumination (shape is (m,)). If not in the list points are actually in the dark.
    """
    # Compute light vectors (starting at the point on the surface and ending at the light source)
    L = s - M
    # Compute illumination use Diffuse Lighting Model (simple dot product)
    lambert = projection(L,N)
    # Find points on the surface that are actually in the light (others are in the dark, negative value for illumination)
    light_indexes = np.argwhere(lambert>0).T
    
    return lambert,light_indexes


def pixels(M,shades,indexes,frame_height,frame_width,size,zoom):
    """Make of projection of a set of 3D illuminated points onto a 2D screen.

    Args:
        M (array[float]): Set of 3D points to be projected (shape must be (n,3)).
        shades (array[float]): Illumination values for each point of the set M (shape must be (n,)).
        indexes (array[float]): Indexes of the points that are illuminated (shape must be (m,)).
        frame_height (int): Height of the 2D screen.
        frame_width (int): Width of the 2D screen.
        size (float): Maximum Size of 3D object.
        zoom (float): Zoom factor.

    Returns:
        M_pixels (array[float]): 2D grayscale image (shape is (frame_height,frame_width)).
    """
    # Initialize 2D screen
    M_pixels = np.zeros((frame_height,frame_width))

    # Map 3D points to the 2D pixels (contained in (X,Y) plane)
    ### (X,Y) 3D positions are mapped to position on the screen (row,column) 
    x_donut = (np.floor(
                    (frame_width/2)+
                    (zoom*frame_width/size)*M[:,0])).astype('int')
    y_donut = (np.floor(
                    (frame_height/2)-
                    (zoom*frame_height/size)*M[:,1])).astype('int')
    ### Filter out points that end up outside the screen
    x_indexes = np.where(np.logical_or( x_donut<0 , x_donut >= frame_width) )[0]
    y_indexes = np.where(np.logical_or( y_donut<0 , y_donut >= frame_height)  )[0]
    xy_indexes = np.concatenate([x_indexes,y_indexes])

    # Make sure the brightest points is represented on the screen
    # Points that are in the dark or outside the screen are ignored
    valid_index = np.setdiff1d(indexes,xy_indexes)
    for idx in valid_index:
        x = x_donut[idx]
        y = y_donut[idx]
        M_pixels[y,x] = np.maximum(shades[idx],M_pixels[y,x])

    return M_pixels