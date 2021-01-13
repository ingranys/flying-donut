
import warnings
warnings.filterwarnings("ignore",category=UserWarning)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def points(M,azimut=None,elevation=None,distance=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(M[:,0],M[:,1],M[:,2])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_xlim([-10,10])
    ax.set_ylim([-10,10])
    ax.set_zlim([-10,10])
    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation
    if distance :
        ax.dist = distance
    plt.show()


def vectors(M,V,azimut=None,elevation=None,distance=None,length=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(M[:,0],M[:,1],M[:,2],V[:,0],V[:,1],V[:,2])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_xlim([-10,10])
    ax.set_ylim([-10,10])
    ax.set_zlim([-10,10])
    if length:
        ax.length = length
    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation
    if distance :
        ax.dist = distance
    plt.show()


def colors(M,colors,azimut=None,elevation=None,distance=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(M[:,0],M[:,1],M[:,2],c=colors)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_xlim([-10,10])
    ax.set_ylim([-10,10])
    ax.set_zlim([-10,10])
    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation
    if distance :
        ax.dist = distance
    plt.show()


def image(pixels):
    y, x = pixels.shape
    plt.imshow(pixels,interpolation='none',cmap='gray',extent=[0,x,0,y],aspect=2)
    plt.show()

def update3d(i, rotations, function, scat):
    donut = np.array(scat._offsets3d).T
    rotated_donut = function(donut,rotations)
    scat._offsets3d = (rotated_donut[:,0],rotated_donut[:,1],rotated_donut[:,2])
    return scat

def animate3d(donut,rotations,function,duration,interval,azimut=None,elevation=None,distance=None):
    n_frames = int(duration*1000/interval)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    scat = ax.scatter(donut[:,0], donut[:,1], donut[:,2])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_xlim([-10,10])
    ax.set_ylim([-10,10])
    ax.set_zlim([-10,10])

    if azimut :
        ax.azim = azimut
    if elevation :
        ax.elev = elevation
    if distance :
        ax.dist = distance

    ani = animation.FuncAnimation(fig, update3d, frames=n_frames, interval=interval, 
                                        fargs=(rotations,function,scat))
    plt.show()