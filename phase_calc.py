import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('directory')
args=parser.parse_args()

directory=args.directory

#set params

steps=301
traj_step_length=1000000
no_lipids=4096
no_atoms=8192


logfilename=directory+"log.dat"
trajfilename=directory+"trajectory.lammpstrj"



#open file----------------------------------
def open_file(filename):

    name=open(filename, "r")
    return name

#get line of file---------------------------
def get_line(name):

    line=name.readline()
    return line 

#check for line before data starts----------
def check_log_start(line):

    if 'Temp' in line:
        return True
    else:
        return False

#see if timestep occurs in traj file
def check_step(line, x):

    newline=line.split()
    step=float(newline[0])

    if step%x == 0:
        return True
    else:
        return False

#obtain temp from each line-----------------
def get_temp(line):

    stripped_line=line.strip()
    data=stripped_line.split()
    temp=float(data[4])
    return temp

#obtain press from each line-----------------
def get_press(line):

    stripped_line=line.strip()
    data=stripped_line.split()
    press=float(data[5])
    return press

#add to temp array--------------------------
def add_temp(temp_array,temp,i):

    temp_array[i]=temp

#add to press array-------------------------
def add_press(press_array,press,i):

    press_array[i]=press

#check for line after data ends-------------
def check_log_end(line):

    if 'Loop time' in line:
        return True
    else:
        return False

#get temps from log file--------------------
def read_temp_press():
    #initialize temperature array
    temp_array=np.zeros((steps))
    press_array=np.zeros((steps))
    #get temperatures from log file
    log=open_file(logfilename)
    line=get_line(log)
    i=0
    while line != '':
        line=get_line(log)
        if check_log_start(line) == True:
            #line=get_line(log) #skips timestep 0 where temp=0
            line=get_line(log)
            while check_log_end(line) == False:
                #print(line.split()[0])
                if check_step(line,traj_step_length) == True:
                    #obtain temp and pressure
                    temp=get_temp(line) 
                    add_temp(temp_array,temp,i)
                    press=get_press(line)
                    add_press(press_array,press,i)
                    i+=1
                line=get_line(log)
            else:
                break
        #else: 
           # print('Yet to reach data', line)
    #print(temp_array)
    return temp_array, press_array

#check for start of timestep traj-----------
def check_traj_start(line):

    if 'ITEM: ATOMS' in line:
        return True
    else:
        return False

#check for end of timestep data------------
def check_traj_end(line):

    if 'ITEM: TIMESTEP' in line:
        return True
    else:
        return False

#check if line is data for top atom
def check_atom_top(line):

    data=line.split()
    if int(data[2])==1:
        return True
    else:
        return False

#check if top atom is extended
def extend_check(line):

    data=line.split()
    z=data[5]
    #print(float(z))
    if float(z) >= 1.4:
        return True
    else:
        return False

#add to count of extended lipid
def add_count(mag_array,j):

    mag_array[j]=mag_array[j]+1

#calc frac of extended in timestep---------
def norm_mag(mag_array,j):

    mag_array[j]=mag_array[j]/no_lipids
    return mag_array

#calc hex of single atom-------------------
def add_hex_mod(line,hex_array,j):

    data=line.split()
    real_hex=float(data[6])
    im_hex=float(data[7])
    hex_mod=real_hex**2 + im_hex**2
    #print(j)
    hex_array[j]=hex_array[j]+hex_mod

#average hex mods in timestep--------------
def norm_hex_avg(hex_array,j):

    hex_array[j]=hex_array[j]/no_lipids
    return hex_array

#calc phase parameters---------------------
def calcs():

    mag_array=np.zeros(steps) #array for % of lipids extended
    hex_array=np.zeros(steps)  #array for avg modulus of hexatic order
    traj=open_file(trajfilename) #trajectory data file object
    line=get_line(traj)
    j=0 #timestep index
    #k=0 #debugging index
    #check for end of file
    while line != '':
        line=get_line(traj)
        #check for beginning of next timestep data
        if check_traj_start(line) == True:
            #print('new line', k)
            #k+=1
            line=get_line(traj)
            #verify still in timestep data and not at end of file
            while check_traj_end(line) == False and line != '':
                #print(line)
                #if true, then check for extended conformation
                if check_atom_top(line) == True:
                    if extend_check(line) == True:
                        mag_array[j]+=1
                        #print('+1')
                    else:
                        mag_array[j]-=1
                        #print('-1')
                #else, check hex order of bottom atom
                else:
                    add_hex_mod(line,hex_array,j)
                #get next line
                line=get_line(traj)
            #end of timestep reached, normalize averages add to count
            else:
                norm_mag(mag_array,j)
                #print(mag_array[j])
                norm_hex_avg(hex_array,j)
                #print(j)
                j+=1
                #break
    
    return mag_array, hex_array


#find discontinuities in hex_phase
def phase_change_calc(temp_array, press_array, hex_array):

    f=open(directory+"phase_change_info.txt", "w")
    f.write("step Temp  Press  change in hex phase  timestep\n")
    
    for i in range(len(hex_array)):
        if i>0:
            if abs(hex_array[i]-hex_array[i-1]) > 0.1:
                f.write(str(i) + ' ' + str(temp_array[i]) +' '+ str(press_array[i])+' '+ str(hex_array[i]-hex_array[i-1]) +'\n')
                #print('hex phase change!\n')
                #print('temp ' + str(temp_array[i]) + ' pressure ' + str(press_array[i]) + '\n')
    f.close()    
    return f



#------------main---------------------------
def main():
    
    #make data arrays        
    temp_array,press_array=read_temp_press()
    mag_array, hex_array=calcs()
    
    #remove timestep 0 data
    temp_array=np.delete(temp_array,0,axis=None)
    press_array=np.delete(press_array,0,axis=None)
    mag_array=abs(mag_array)
    mag_array=np.delete(mag_array,0,axis=None)
    hex_array=np.delete(hex_array,0,axis=None)
    
    #save temp and press arrays 
    np.save(directory+'temp_data.npy',temp_array)
    np.save(directory+'press_data.npy',press_array)
    np.save(directory+'mag_data.npy',mag_array)
    np.save(directory+'hex_data.npy',hex_array)

    #find points of phase change
    phase_change_calc(temp_array, press_array, hex_array)
    
    #plot magnetization phase diagram
    plt.scatter(temp_array, mag_array)
    plt.xlabel('Temp')
    plt.ylabel('Magnetization')
    #plt.show()
    plt.savefig(directory+'/magnetization_phase_diagram.png')
    
    #clear plot space
    plt.clf()
    
    #plot hexatic order phase diagram
    plt.scatter(temp_array, hex_array)
    plt.xlabel('Temp')
    plt.ylabel('$|\\psi_{6}|^{2}$')
    #plt.show()
    plt.savefig(directory+'/hexatic_order_phase_diagram.png')
    
    #clear plot space
    plt.clf()
    
    #plot both
    plt.scatter(temp_array,mag_array)
    plt.scatter(temp_array,hex_array)
    plt.xlabel('Temp')
    plt.ylabel('phase parameter')
    plt.legend(['magnetization','hexatic order'], loc='upper right')
    plt.savefig(directory+'/combo_phase_diagram.png')    
    
    #plt.show()

    t=np.linspace(1,(steps-1),num=(steps-1))

    #clear plot space
    plt.clf()

    #plot P vs t

    pmean=np.mean(press_array)

    plt.scatter(t,press_array)
    plt.axhline(y=pmean,color='r',linewidth=2)
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.savefig(directory+'/P_vs_t.png')

    #plt.show()

    #clear plot space
    plt.clf()
    #plot T vs t
    plt.scatter(t,temp_array)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.savefig(directory+'/T_vs_t.png')

    #plt.show()

#run main
main()
