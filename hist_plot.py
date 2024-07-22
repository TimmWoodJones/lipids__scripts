import numpy as np
import argparse
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser()

parser.add_argument('directory')
parser.add_argument('step')
parser.add_argument('subj')


args=parser.parse_args()

directory=args.directory
step=args.step
subj=args.subj

if subj=='dens':
    path=directory+'dens_hist_frames/'
elif subj=='hex':
    path=directory+'hex_mod_hist_frames/'
elif subj=='spin':
    path=directory+'spin_hist_frames/'

if os.path.exists(path)==False:
    os.system('mkdir ' +path)



def open_dens():

    f=np.load(directory+'density_hist.npy')
    return f

def open_spin():
    f=np.load(directory+'spin_hist.npy')
    return f

def open_hex():
    f=np.load(directory+'bot_hex_mod_data.npy')
    return f


def get_step_data(f,step):

    x=f[:,(step-1)]
    x=x[x!=0]
    return x


def plot_dens(u,t):

    fig, ax=plt.subplots()

    
    plt.hist(u,range=[0,30],bins=50)
    fig1=plt.gcf()
    plt.ylim((0,30))
    if step != 'all':
        plt.show()
        t=step
    fig1.savefig((path+'dens_hist_frame_'+str(t)+'.png'))

def plot_spin(u,t):

    fig, ax=plt.subplots()

    plt.hist(u,range=[-1,1],bins=25)
    fig1=plt.gcf()
    if step != 'all':
        plt.show()
        t=step
    fig1.savefig((path+'spin_hist_frame_'+str(t)+'.png'))

def plot_hex(u,t):

    fig, ax=plt.subplots()

    plt.hist(u,range=[0,1],bins=25)
    fig1=plt.gcf()
    plt.ylim((0,1000))
    if step !='all':
        plt.show()
        t=step
    fig1.savefig((path+'hex_mod_hist_frame_'+str(t)+'.png'))




if step=='all':
    
    if subj=='dens':
        f=open_dens()
        plot=plot_dens

    if subj=='hex':
        f=open_hex()
        plot=plot_hex

    if subj=='spin':
        f=open_spin()
        plot=plot_spin

    for t in range(300):
        
        data=get_step_data(f,t)
        plot(data,t)        




else:

    t=0
    step=int(step)

    if subj =='dens':
        f=open_dens()
        data=get_step_data(f,step)
    #print(data)
        plot_dens(data,t)

    if subj =='hex':
        f=open_hex()
        data=get_step_data(f,step)
    #print(data)
        plot_hex(data,t)

    if subj =='spin':
        f=open_spin()
        data=get_step_data(f,step)
    #print(data)
        plot_spin(data,t)



#f=open_file()
#data=get_step_data(f,step)
#plot_dens(data)



