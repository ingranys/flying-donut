import warnings
warnings.filterwarnings("ignore",category=UserWarning)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def points(M,azimut=None,elevation=None,size=10,title='points'):
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
    y, x = pixels.shape
    plt.imshow(pixels,interpolation='none',cmap='gray',extent=[0,x,0,y],aspect=2)

    plt.show()


def update3d(i, rotations, function, scat):
    donut = np.array(scat._offsets3d).T
    rotated_donut = function(donut,rotations)
    scat._offsets3d = (rotated_donut[:,0],rotated_donut[:,1],rotated_donut[:,2])

    return scat


def animate3d(donut,rotations,function,n_frames,azimut=None,elevation=None,size=10,title='animation'):
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