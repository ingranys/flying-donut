import numpy as np
from scipy.spatial.transform import Rotation as R


def base():
    X = np.array([1,0,0])
    Y = np.array([0,1,0])
    Z = np.array([0,0,1])

    return X, Y, Z


def donut(V_R1,V_R2,V_theta,n_theta,V_phi,n_phi):
    n_points = n_theta*n_phi

    theta_angles = np.linspace(0,2*np.pi,n_theta,endpoint=False)
    phi_angles = np.linspace(0,2*np.pi,n_phi,endpoint=False)


    M_circle = np.array([R.from_rotvec(theta_angle*V_theta).apply(V_R1) for theta_angle in theta_angles])
    M_translated_circle = M_circle + V_R2
    #points(np.vstack((M_circle,M_translated_circle)),-90,135,5)
        
    phi_rotations = [R.from_rotvec(phi_angle*V_phi) for phi_angle in phi_angles]
    M_rotated_circles = np.array([phi_rotation.apply(M_translated_circle) for phi_rotation in phi_rotations])
    
    M_donut = M_rotated_circles.reshape(n_points,3)
    V_normals = np.array([phi_rotation.apply(M_circle) for phi_rotation in phi_rotations]).reshape(n_points,3)

    return M_donut,V_normals



def rotations(V_A,angle_A,V_B,angle_B):
    R_A = R.from_rotvec(angle_A*V_A)
    R_B = R.from_rotvec(angle_B*V_B)

    return [R_A, R_B]


def rotate(M,rotations):
    for rotation in rotations:
        M = rotation.apply(M)
    
    return M


def normalize(V):
    V_norms =  np.linalg.norm(V, ord=2,axis=1)[:,None]

    return V/V_norms


def projection(V1,V2):
    V1_normalized = normalize(V1)
    V2_normalized = normalize(V2)

    sumproduct =  np.einsum('ij, ij->i', V1_normalized, V2_normalized)

    return sumproduct


def shades(M,N,s):
    L = s - M
    return projection(L,N)