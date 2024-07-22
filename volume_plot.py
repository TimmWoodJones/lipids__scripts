import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('directory')
args=parser.parse_args()

directory=args.directory

volume=np.load(directory+'vol_data.npy')

t=np.linspace(1,int(len(volume)),num=len(volume))

diff=np.zeros((int(len(volume)-1)))

for i in range(len(diff)):
    diff[i]=volume[i+1]-volume[i]

dmax=np.argmax(diff)

plt.scatter(t,volume,s=5)
plt.vlines(dmax,volume.min(),volume.max(),colors='k')
plt.text(dmax,volume.max(),str(dmax))
plt.show()

plt.close()
