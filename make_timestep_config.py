import numpy as np
import argparse
#from pathlib import Path
import os


parser=argparse.ArgumentParser()
parser.add_argument('press')
parser.add_argument('timestep')
args=parser.parse_args()

press=args.press
timestep=int(args.timestep)

directory='TP_space/P'+press+'/'

dat=open(directory+'heating/trajectory.lammpstrj','r')

newdir=directory+'constantT/'+str(timestep)+'_heat_step/'

if os.path.exists(newdir)==False:
    os.makedirs(newdir)

conf=open(newdir+'conf.lammps','w')

log=open(directory+'heating/log.dat','r')

temp_info=open(newdir+'temp_info.txt','w')

def start_conf(f):

    lines=['LAMMPS data file\n', '\n', '8192 atoms\n', '4096 bonds\n', '\n', '2 atom types\n', '2 bond types\n', '\n', '0 116.847 xlo xhi\n', '0 116.847 ylo yhi\n', '-2.0 3.0 zlo zhi\n', '\n', 'Masses\n', '\n', '1 1\n', '2 1\n', '#Atom-ID molecule-ID atom-type q x y z\n', 'Atoms\n', '\n']

    f.writelines(lines)



def get_line(f):

    line=f.readline()
    return line

#also use this to check for the end of correct step
def check_step_start(line):

    if 'TIMESTEP' in line:
        return True
    else:
        return False

def check_correct_step(line):

    data=line.split()
    if str(timestep*1000000)==data[0]:
        print('step found!')
        return True
    else:
        return False

def start_data(line):

    if 'ITEM: ATOMS' in line:
        return True
    else:
        return False

def line2list(line):

    data=line.split()
    return data

def write_data(data,f):

    #print(data)

    atom=str(data[0])
    mol=str(data[1])
    atype=str(data[2])
    x=str(data[3])
    y=str(data[4])
    z=str(data[5])
    space=' '

    f.write(atom+space+mol+space+atype+space+str(0)+space+x+space+y+space+z+'\n')


def end_conf(f):

    f.write('\n')
    f.write('Bonds\n')
    f.write('\n')

    #N=8192
    Nmol=4096
    
    for i in range(Nmol):
        if i<Nmol/2:
            btype=1
        else:
            btype=2

        f.write(str(i+1)+' '+str(btype)+' '+str(2*i+1)+' '+str((2*(i+1)))+'\n')

def check_end_file(line):

    if line=='':
        return True
    else:
        return False


#print(timestep*1000000)

start_conf(conf)

k=0

line=get_line(dat)
while check_end_file(line)==False:

    line=get_line(dat)
    if check_step_start(line)==True:
        k+=1
        line=get_line(dat)
        #print(line.split()[0])
        #break
        if check_correct_step(line)==True:
            while start_data(line)==False:
                line=get_line(dat)
            else:
                line=get_line(dat)
                while check_step_start(line)==False:
                    data=line2list(line)
                    write_data(data,conf)
                    line=get_line(dat)

end_conf(conf)

line=get_line(log)
while check_end_file(line)==False:

    line=get_line(log)
    data=line2list(line)
    
    if str(timestep*1000000) in line:
        temp=data[4]
        print('temp is ' + temp)
        break
temp_info.write('temp was ' + temp + ' at step ' + str(timestep))







