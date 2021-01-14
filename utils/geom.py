import numpy as np
from scipy.spatial.transform import Rotation as R


def base():
    X = np.array([1,0,0])
    Y = np.array([0,1,0])
    Z = np.array([0,0,1])

    return X, Y, Z


def donut(R1,R2,V_R,V_theta,n_theta,V_phi,n_phi):
    V_R1 = R1*V_R
    V_R2 = R2*V_R
    n_points = n_theta*n_phi

    theta_angles = np.linspace(0,2*np.pi,n_theta,endpoint=False)
    phi_angles = np.linspace(0,2*np.pi,n_phi,endpoint=False)


    M_circle = np.array([R.from_rotvec(theta_angle*V_theta).apply(V_R1) for theta_angle in theta_angles])
    M_translated_circle = M_circle + V_R2
    M_circles = np.vstack((M_circle,M_translated_circle))
        
    phi_rotations = [R.from_rotvec(phi_angle*V_phi) for phi_angle in phi_angles]
    M_rotated_circles = np.array([phi_rotation.apply(M_translated_circle) for phi_rotation in phi_rotations])
    
    M_donut = M_rotated_circles.reshape(n_points,3)
    V_normals = np.array([phi_rotation.apply(M_circle) for phi_rotation in phi_rotations]).reshape(n_points,3)

    return M_donut,V_normals,M_circles



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
    lambert = projection(L,N)
    light_indexes = np.argwhere(lambert>0).T
    return lambert,light_indexes


def pixels(M,shades,indexes,frame_height,frame_width,size,zoom):
    M_pixels = np.zeros((frame_height,frame_width))

    x_donut = (np.floor(
                    (frame_width/2)+
                    (zoom*frame_width/size)*M[:,0])).astype('int')
    y_donut = (np.floor(
                    (frame_height/2)-
                    (zoom*frame_height/size)*M[:,1])).astype('int')

    x_indexes = np.where(np.logical_or( x_donut<0 , x_donut >= frame_width) )[0]
    y_indexes = np.where(np.logical_or( y_donut<0 , y_donut >= frame_height)  )[0]
    xy_indexes = np.concatenate([x_indexes,y_indexes])

    valid_index = np.setdiff1d(indexes,xy_indexes)
    for idx in valid_index:
        x = x_donut[idx]
        y = y_donut[idx]
        M_pixels[y,x] = np.maximum(shades[idx],M_pixels[y,x])

    return M_pixels