import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
#yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from numpy import *

def get_fn(i):
    a0=''
    if (i<10):
      a0='000'
    if (10<=i<100):
      a0='00'
    if (100<=i<999):
      a0='0'
    filen='DD'+a0+str(i)+'/sb_'+a0+str(i)
    return filen

def _number_density(field,data):
    return abs(data['density']/YTQuantity(1.67e-24,'g'))


yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

profiles=[]
labels=[]
plot_specs=[]


def see(i):
  fn = get_fn(i)
  ds = yt.load(fn)
  ad=ds.all_data()
  r=400.
  y='metallicity'
  x='radius'
  theta_factor = array([0, 0.1, 0.2, 0.3,0.4 , 0.5])
  profiles=[]
  labels=[]
  plot_specs=[]
  R1_theta=[]
  Rmax_theta=[]
  for n in range(len(theta_factor)):
    theta=3.1415925*theta_factor[n]
    start = ((0.0, "kpc"), (0.0, "kpc"), (0.0, "kpc"))
    end = ((r * sin(theta), "kpc"), (r*sin(theta), "kpc"), (r*cos(theta), "kpc"))
    ray = ds.r[start:end]
    nbins=32
    prof = yt.create_profile(data_source=ray,bin_fields=x, fields=y, n_bins=nbins, logs=None)

    print("prof.x=",prof.x.in_units('kpc'))
    print ("prof[y]=",prof[y])
   
    ymax= max(prof[y])
    ymin= min(prof[y])
    print('ymax=',ymax)
    print('ymin=',ymin)
    R1 = 0.
    Rmax=0.
    for m1 in range(nbins):
       if prof[y][m1]>1.5 * 0.2:
          Rmax=prof.x[m1].in_units('kpc').round(2)
       if prof[y][m1]>0.8* ymax: 
          R1=prof.x[m1].in_units('kpc').round(2)
#    profiles.append( prof)
    R1_theta.append(R1)
    Rmax_theta.append(Rmax)
    time  = ds.current_time.in_units('Myr').round(2)
  f=open('Rmax_t.dat','a')
  print (time, Rmax_theta[0], Rmax_theta[1], Rmax_theta[2], Rmax_theta[3],  Rmax_theta[4], Rmax_theta[5],   R1_theta[0], R1_theta[1],  R1_theta[2], R1_theta[3], R1_theta[4], R1_theta[5], file=f)
  f.close()


num=range(10,800,30)
for i in num:
   see(i)
    
