import numpy as np
import matplotlib.pyplot as plt
import argparse

#get directory from arguments

parser=argparse.ArgumentParser()

parser.add_argument('directory')

parser.add_argument('-m','--mode',default='all')

args = parser.parse_args()

directory=args.directory
mode=args.mode


#get step where phase changes

f=open(directory+'phase_change_info.txt')

f.readline()
data=f.readline()
data=data.split()
step=data[0]

print(step)

f.close()

#open trajectory file

f=open(directory+'trajectory.lammpstrj',"r")


xtop=np.load(directory+'top_x_data.npy')
ytop=np.load(directory+'top_y_data.npy')
spin_dat=np.load(directory+'spin_data.npy')
xbot=np.load(directory+'bot_x_data.npy')
ybot=np.load(directory+'bot_y_data.npy')
hex_dat=np.load(directory+'bot_hex_mod_data.npy')


#define parameters

dx=9 #grid spacing needs to be tested

L=117 #side length of square system rounded up to nearest integer

N_grid=int(L/dx) #number of grids in a single axis

density=np.zeros((N_grid,N_grid))


#write functions to check for timesteps

def check_start(x):

    if 'ITEM: ATOMS' in x:
        return True
    else:
        return False

def check_end(x):

    if 'ITEM: TIMESTEP' in x:
        return True
    else:
        return False

def phase_change_step(x,step):

    y=step*1000000    
    if str(y) in x:
        return True
    else:
        return False


def check_last_step(x):

    if '300000000' in x:
        return True
    else:
        return False


def check_bot(x):

    #print(x)

    if int(x[2])==2:
        return True
    else:
        return False

def get_grid_indices(data):

    xcoor=float(data[3])
    ycoor=float(data[4])

    x=int(np.floor(xcoor/dx))
    y=int(np.floor(ycoor/dx))

    #print(xcoor, ycoor)
    #print(x,y)


    return x,y

fig, ax=plt.subplots()


#calc loop
def calc_all_steps(density):
    t=0

    line=f.readline()
    while (line != ''):

        line=f.readline()
        if check_start(line)==True:
        
            line=f.readline()

            while (check_end(line)==False and line != ''):

                data=line.split()

                if check_bot(data)==True:

                #print(data[0])

                    x,y = get_grid_indices(data)

                #print(x,y)
                #break

                    density[x,y]+=1

                line=f.readline()

            else:
                t+=1
                print(t)
                density=np.zeros((N_grid,N_grid))
                density=density.reshape(N_grid**2)
                density=density[density !=0]
                print('size of density array')
                print(len(density))
                density=density/(dx**2)

                ax.hist(density, bins=100)

                if t==300:

                    plt.savefig(directory+'last_step_hist.png')

                density=np.zeros((N_grid,N_grid))

def calc_phase_change_step(density):

    #t=0

    line=f.readline()    
    while line != '':

        line=f.readline()
        
        if phase_change_step(line,step)==True:

            line=f.readline()

            if check_start(line) == True:
            
                line=f.readline()
           
                while check_end(line) == False:           

                    line=f.readline()

                    data=line.split()

                    if check_bot(data)== True:

                        x,y = get_indices(data)

                        density[x,y]+=1
    
                #else:
                   

                else:
                    print('done reading file')
                    density=density[density !=0]
                    density=density/(dx**2)

                    ax.hist(density,bins=100)
                    plt.show()

                    plt.savefig(directory+'phase_change_hist.png')
                    plt.close()

                    break

    #return density

#choose which calc to make


if mode =='all':
    calc_all_steps(density)
if mode =='change':
    calc_phase_change_step(density)



#density=density[density != 0]
#density=density/(dx**2)

            #ax.imshow(density, cmap=plt.cm.plasma)
            #plt.show()
#ax.hist(density, bins=200)
#plt.show() 
#if t==300:

                #plt.show()
#plt.savefig(directory+'last_step_hist.png')

#plt.close()



#for each timestep in trajectory file, calculate # of particles in each grid
##start with grid spacing of 5*sigma

#maybe first just try with a single timestep to make sure it all works
##then find ways to get all the statistics for each simulation

#
