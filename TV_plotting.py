import numpy as np
import matplotlib.pyplot as plt
import argparse

import os

parser = argparse.ArgumentParser()
parser.add_argument('min')
parser.add_argument('max')
parser.add_argument('inc')
parser.add_argument('mode')
parser.add_argument('cmode')


args=parser.parse_args()

minimum=float(args.min)
maximum=float(args.max)
inc=float(args.inc)
mode=args.mode
cmode=args.cmode

N=int(np.round((maximum-minimum)/inc + 1))

#temp=np.zeros((300))
#vol=np.zeros((300))

#V=np.zeros((int(4*N)))
#T=np.zeros((int(4*N)))
#diff=np.zeros((int(2*N)-1))

colors=['red', 'blue', 'green', 'black', 'cyan', 'magenta', 'yellow'] 

markers=['.','v','^','x','d','s','2']

cmap='plasma'

size=5 #point size

#for i in range(N):

    #num=inc*(i+1)

    #num=np.around(num,decimals=2)



    #if mode == 'heat' or mode == 'both':

        #directory='TP_space/P'+str(num)+'/heating/'

        #calc(directory):




def dir_check(directory):

    if os.path.exists(directory)==True and os.path.exists(directory+'temp_data.npy')==True and os.path.exists(directory+'vol_data.npy')==True and os.path.exists(directory+'mag_data.npy')==True:

        return True


def calc(directory):
        #temp=np.zeros((300))
        #vol=np.zeros((300))

        temp=np.load(directory+'temp_data.npy')
        vol=np.load(directory+'vol_data.npy')
        if cmode=='mag':
            cdata=np.load(directory+'mag_data.npy')
        if cmode=='hex':
            cdata=np.load(directory+'hex_data.npy')
        return temp, vol, cdata

        #color=colors[i%int(len(colors))]

        #plt.plot(vol,temp,color=color)

            #diff=np.zeros((int(len(vol)-1)))

            #for j in range(len(diff)):

                #diff[j]=vol[j+1]-vol[j]

        #maxdiff=diff.max()
    
        #index=np.argwhere(diff==maxdiff)

        #V[2*i]=vol[index]
        #V[2*i+1]=vol[index+1]
        #T[2*i]=temp[index]
        #T[2*i+1]=temp[index+1]

        

#sorted_indices=V.argsort()
#V=V[sorted_indices]
#T=T[sorted_indices]

k=0

for i in range(N):
    #print(k)
    num=inc*(i+1)

    num=np.around(num,decimals=2)

    if mode == 'heat' or mode == 'all':

        directory='TP_space/P'+str(num)+'/heating/'
            
        if dir_check(directory)==True:
            temp,vol,cdata=calc(directory)
            #color=colors[i%int(len(colors))]
            marker=markers[i%int(len(markers))]
            plt.scatter(vol,temp,c=cdata,marker=marker,cmap=cmap,s=size,vmin=0,vmax=1)
            k+=1

    if mode == 'cool' or mode == 'all':

        directory='TP_space/P'+str(num)+'/cooling/'
        
        if dir_check(directory)==True:
            temp,vol,cdata=calc(directory)
            #color=colors[i%int(len(colors))]
            marker=markers[i%int(len(markers))]
            plt.scatter(vol,temp,c=cdata,marker=marker,cmap=cmap,s=size,vmin=0,vmax=1)
            k+=1

    if mode == 'const' or mode == 'all':

        obj=os.scandir('TP_space/P'+str(num)+'/constantT/')
        for d in obj:
            if d.is_dir()==True:
                step=d.name
                directory='TP_space/P'+str(num)+'/constantT/'+step+'/'
                if dir_check(directory)==True:
                    temp,vol,cdata=calc(directory)
                    #color=colors[i%int(len(colors))]
                    marker=markers[i%int(len(markers))]
                    plt.scatter(vol,temp,c=cdata,marker=marker,cmap=cmap,s=size,vmin=0,vmax=1)
                    k+=1



#V=V[V!=0]
#T=T[T!=0]

#plt.scatter(V,T,c='k')

#plt.xscale('log')
plt.xlabel('Volume')
plt.ylabel('Temperature')
plt.title('T vs. V with constant P lines')

#plt.xlim(4500,7000)

fig1=plt.gcf()

fig1.savefig('TV_plot_'+mode+'_'+cmode+'_color.png')

#plt.colorbar()
plt.show()


