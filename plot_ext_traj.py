import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import time
import os

parser=argparse.ArgumentParser()

parser.add_argument('press')
parser.add_argument('mode')
parser.add_argument('step')

args=parser.parse_args()

press=args.press
mode=args.mode

step=args.step

#cutoffs for spin up and spin down, respectively
zmax=1.8
zmin=1


if mode=='heat':

    directory='TP_space/P'+press+'/heating/'

if mode=='cool':

    directory='TP_space/P'+press+'/cooling/'

path=directory+'extension_frames/'


if os.path.exists(path)==False:
    os.system('mkdir ' + path)



x=np.load(directory+'top_x_data.npy')
y=np.load(directory+'top_y_data.npy')
z=np.load(directory+'top_z_data.npy')

#zmin=min(z)


def plot_step(i,step):

    xdat=x[:,i]
    ydat=y[:,i]
    zdat=z[:,i]

    #print(xdat)
    #print(ydat)

    fig, ax = plt.subplots()

    ax.scatter(xdat,ydat,c=zdat,cmap='plasma',s=10,vmin=zmin,vmax=zmax)
    #plt.colorbar()
    plt.gca().set_aspect('equal')
    plt.gca().set_facecolor('black')
    #plt.xlim(0, 107)
    #plt.ylim(0, 107)
    #plt.axis('off')
    
    fig=plt.gcf()
    ax=plt.gca()
    if step=='all':
        plt.savefig(path+'ext_frame_'+str(i)+'.png')
    else:
        plt.show()

    #plt.close()
    #return ax
    #return fig, ax

    #fig.show(block=False)
    
    #plt.close()

if step=='all':

    frames=[]

    for i in range(300):

        j=i+1
        print(j)
        plot_step(j,step)

        #plt.figure(fig)
        #plt.
        #plt.ion()
        #plt.show()
        #plt.close()
        #frame=fig 
        #frames.append(frame)
        #plt.close()


    #ani=animation.ArtistAnimation(fig=fig, artists=frames, interval=300)

    #name=(path+'hex_proj_movie.mp4')

    #ani.save(filename=name, writer="pillow")


else:

    i=int(step)

    plot_step(i,step)

    #plt.figure(fig)

    #plt.show(block=True)

