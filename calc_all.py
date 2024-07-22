import argparse
import numpy as np
import os

parser=argparse.ArgumentParser()
parser.add_argument('min')
parser.add_argument('max')
parser.add_argument('inc')
parser.add_argument('mode')

args=parser.parse_args()

#directory=args.directory
minim=float(args.min)
maxim=float(args.max)
inc=float(args.inc)
mode=args.mode

N=int(np.round((maxim-minim)/inc+1))

for i in range(N):

    num=minim+inc*(i)
    
    num=np.around(num,decimals=2)
    
    print(num)

    if mode=='heat' or mode=='all':

        directory='TP_space/P'+str(num)+'/heating/'

        #print('calculating phase data for P' + str(num))
        os.system('python phase_calc.py ' +directory)
        #print('calculating density for P' + str(num))
        os.system('python hist_calcs.py ' +directory)

    if mode=='cool' or mode=='all':

        directory='TP_space/P'+str(num)+'/cooling/'

        #print('calculating phase data for P' + str(num))
        os.system('python phase_calc.py ' +directory)
        #print('calculating density for P' + str(num))
        os.system('python hist_calcs.py ' +directory)
        


    if mode=='const' or mode=='all':

        obj=os.scandir('TP_space/P'+str(num)+'/constantT/')

        for d in obj:
            if d.is_dir()==True:
                step=d.name
                directory='TP_space/P'+str(num)+'/constantT/'+step+'/'

                os.system('python phase_calc.py ' +directory)

                os.system('python hist_calcs.py ' +directory)




