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




if mode=='heat':

    directory='TP_space/P'+press+'/heating/'

if mode=='cool':

    directory='TP_space/P'+press+'/cooling/'

path=directory+'hex_mod_frames/'

if os.path.exists(path)==False:
    os.system('mkdir ' + path)



x=np.load(directory+'bot_x_data.npy')
y=np.load(directory+'bot_y_data.npy')
h=np.load(directory+'bot_hex_mod_data.npy')




def plot_step(i):

    xdat=x[:,i]
    ydat=y[:,i]
    hdat=h[:,i]

    #print(xdat)
    #print(ydat)

    fig, ax = plt.subplots()

    ax.scatter(xdat,ydat,c=hdat,cmap='rainbow',s=10,vmin=0,vmax=1)
    #plt.colorbar()
    plt.gca().set_aspect('equal')
    plt.gca().set_facecolor('black')
    #plt.xlim(0, 107)
    #plt.ylim(0, 107)
    #plt.axis('off')
    
    fig=plt.gcf()
    ax=plt.gca()
    #plt.show()
    plt.savefig(path+'hex_frame_'+str(i)+'.png')
    #plt.close()
    #return ax
    #return fig, ax

    #fig.show(block=False)
    
    plt.close()

if step=='all':

    frames=[]

    for i in range(300):

        j=i+1
        print(j)
        plot_step(j)

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

    plot_step(i)

    #plt.figure(fig)

    #plt.show(block=True)

