import numpy as np
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('directory')

args=parser.parse_args()

directory=args.directory

dx=5

L=117 #side lenght in units sigma

Lx=L
Ly=L

Ngrid=int(L/dx) #number of grids per side length

Np=4096 #number of particles

Nx=Ngrid #number of grids on x axis
Ny=Ngrid #number of grids on y axis

xmin=0 #min x coor
ymin=0 #min y coor
xmax=Ngrid-1 #max x coor of last grid
ymax=Ngrid-1 #max y coor of last grid


density=np.zeros((Ngrid,Ngrid))
x=np.zeros((Np))
y=np.zeros((Np))

botxdat=np.load(directory+'bot_x_data.npy')
hexdat=np.load(directory+'bot_hex_mod_data.npy')


def open_traj():

    f=open(directory+'trajectory.lammpstrj','r')

    return f

def get_line(f):

    line=f.readline()
    return line

def line2list(line):

    data=line.split()
    return data

def check_traj_start(line):

    if 'ITEM: ATOMS' in line:
        return True
    else:
        return False

def check_traj_end(line):

    if 'ITEM: TIMESTEP' in line:
        return True
    else:
        return False

def check_bot(data):
    #print(data)
    if int(data[2])==2:
        return True
    else:
        return False

def get_indices(data):

    x=float(data[3])
    y=float(data[4])

    return x,y

def norm_density(u):

    u=u.reshape((Nx*Ny))
    u=u/(dx**2)
    return u

def open_dat_file():

    f=open(directory+'density_hist.dat','w')
    return f

def write_data(f,u,t):
    #write timestep #
    f.write(str(t))
    f.write('\n')
    #write densities 
    u=np.array2string(u)
    u.strip('[')
    u.strip(']')
    f.write(u)
    f.write('\n')

    return f

def reset(u):

    u=np.zeros((Nx,Ny))
    return u

def read_timestep(f,x,y):

    i=0
    line=get_line(f)
    while check_traj_end(line) == False and line!='':
        data=line2list(line)
        if check_bot(data) == True:
            x[i],y[i] = get_indices(data)
            i+=1
        line=get_line(f)
        

    

    return x,y


def grid_measure(x,y):

    xmin=x.min()
    ymin=y.min()

    xmax=x.max()
    ymax=y.max()

    Lx=xmax-xmin
    Ly=ymax-ymin

    Nx=int(np.ceil(Lx/dx) +int(27/dx)) 
    Ny=int(np.ceil(Ly/dx) +int(27/dx))

    return xmin,ymin,Nx,Ny

def dens_calc(xmin,ymin,Nx,Ny,x,y):

    dens=np.zeros((Nx,Ny))

    for i in range(Np):

        x_grid=x[i]-xmin
        y_grid=y[i]-ymin

        xcoor=int(np.floor(x_grid/dx))
        ycoor=int(np.floor(y_grid/dx))

        #print(xcoor)
        #print(int(xcoor))

        dens[xcoor,ycoor]+=1

    return dens


def vol_calc(x,y):

    xmin=x.min()
    ymin=y.min()
    xmax=x.max()
    ymax=y.max()

    Lx=xmax-xmin
    Ly=ymax-ymin

    vol=Lx*Ly

    return vol

#main

traj=open_traj()
dat=open_dat_file()
line=get_line(traj)

#master=0
t=0
vol=np.zeros((300))

while line != '':
    if check_traj_start(line) == True:
        x,y=read_timestep(traj,x,y)
        if t==1:
            xmin,ymin,Nx,Ny=grid_measure(x,y)
            #print(xmin,ymin,Nx,Ny)
            master=np.zeros((Nx*Ny,300))
        if t>=1:
            dens=dens_calc(xmin,ymin,Nx,Ny,x,y)
            dens=norm_density(dens)
            vol[t-1]=vol_calc(x,y)
            master[:,t-1]=dens
            #print(dens)
            #print(t)
        
        t+=1

    line=get_line(traj)


#print(master.shape)
np.save(directory+'density_hist.npy',master)
np.save(directory+'vol_data.npy',vol)
traj.close()
dat.close()


