import numpy as np
import argparse 
import matplotlib.pyplot as plt

parser=argparse.ArgumentParser()

parser.add_argument('press')
parser.add_argument('mode')
parser.add_argument('step')
parser.add_argument('subj')

args=parser.parse_args()

press=args.press
mode=args.mode
step=int(args.step)
subj=args.subj

if mode == 'heat':
    directory='TP_space/P'+press+'/heating/'

def load_data(path,step):

    q=np.load(path)
    u=q[:,step]
    return u


if subj == 'dens':
    path=directory+'density_hist.npy'
    cmin=0
    cmax=1


if subj == 'hex':
    path=directory+'hex_mod_hist.npy'
    cmin=0
    cmax=1


if subj == 'spin':
    path=directory+'spin_hist.npy'
    cmin=-1
    cmax=1


data=load_data(path,step)

L=int(np.sqrt(len(data)))

x=np.linspace(1,L,num=L)
y=np.linspace(1,L,num=L)

data=np.reshape(data, (L,L))

plt.pcolor(x,y,data)
plt.show()




