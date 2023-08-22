import matplotlib
matplotlib.use('Agg')
import yt
from yt import *
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *
from yt import YTQuantity

from matplotlib.pyplot import cm



font = {'family' : 'serif',
        'sans-serif':'Helvetica',
#        'weight' : 'bold',
        'size'   : 23}

matplotlib.rc('font', **font)

fig=plt.figure(figsize=(10,8))


r = array([10,20,30,40,50,60,80,100,120,160,200,240])
f=open("Lx_enclosed.dat",'r')
data= loadtxt(f)
f.close()

#print (data[0].shape)
#print (r.shape)
print (data.shape)
#print (data.shape[0])
#print (data.shape[1])

num_col=data.shape[0]
num_row = data.shape[1]
color=cm.cool(np.linspace(0,1, num_col))
m=0
while m< num_col:
   plt.plot(r, data[m][1:],label=str(round(data[m][0],2))+"Gyr", c=color[m])
   m=m+1

plt.legend(loc=4,fontsize=10)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('r  [kpc]')
plt.ylabel("enclosed Lx  [erg/s]")
plt.grid()
plt.savefig("Lx_R_t.png")

plt.clf()
fig=plt.figure(figsize=(10,8))

print (data.T[:][0])
print (data.T[:][10])
plt.plot(data.T[:][0], data.T[:][10])
plt.xlabel("time [Gyr]")
plt.ylabel("Lx  [erg/s]")
plt.yscale('log')
plt.grid()
plt.savefig("Lx_t.png")
 
