import numpy as np
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('press')
parser.add_argument('mode')

args=parser.parse_args()

num=float(args.press)
mode=args.mode


x_data=np.zeros((4096,301))
y_data=np.zeros((4096,301))
hex_data=np.zeros((4096,301))



if mode=='heat':

    directory='TP_space/P'+str(num)+'/heating/'

if mode=='cool':

    directory='TP_space/P'+str(num)+'/cooling/'

def open2read(name):

    f=open(directory+name,'r')

    return f

def open2write(name):

    f=open(directory+name,'w')

    return f

def readlines(f):

    lines=f.readlines()

    return lines







traj=open2read('trajectory.lammpstrj')

new_traj=open2write('hex_proj_traj.lammpstrj')

data_lines=readlines(traj)

step=-1

i=0

for line in data_lines:

    data=line.split()

    if len(data)==9:
        
            #print(data)
            #break
        if data[2]=='2':
            #perform calculation of hex projection of bottom atoms
            new_data=data[0:5]
            new_data[0]=str(int(int(new_data[0])/2))
            new_data=' '.join(new_data)
            hex_proj=data[8]
            new_traj.write(new_data+' '+hex_proj+'\n')

            x_data[i,step]=data[3]
            y_data[i,step]=data[4]
            hex_data[i,step]=hex_proj
            i+=1

    #elif len(data)==2 and data[1]=='TIMESTEP':
        

    elif data[0]=='8192':
        new_traj.write('4096 \n')

    elif len(data)==11:
        new_traj.write('ITEM: ATOMS id mol type x y z \n') #z is the hex_proj
        i=0
        step+=1

    else:
        new_traj.write(line)#+'\n')


np.save(directory+'bot_x_data.npy',x_data)
np.save(directory+'bot_y_data.npy',y_data)
np.save(directory+'bot_hex_proj_data.npy',hex_data)


