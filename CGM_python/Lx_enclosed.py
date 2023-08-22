import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *
from yt import YTQuantity

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

def _metallicity_solar(field,data):
    return data['metal_density']/data['density']/0.01295

yt.add_field('metallicity_solar',function=_metallicity_solar,units="")

def see(i):
  n = 0
#  r = array([10,20,30,40,50,60,80,100,120,160,200,240])
  r = [10,20,30,40,50,60,80,100,120,160,200,240]
  Lx =[]
  fn = get_fn(i)
  ds = yt.load(fn)
  ad = ds.all_data()
  c1=[0.0, 0. ,0.]
  yt.add_xray_emissivity_field(ds, e_min=0.5,e_max= 2, metallicity = ("gas","metallicity_solar"), table_type = 'apec', cosmology =None)

  print ('len r=',len(r))
  m=0
  time = ds.current_time.in_units("Gyr")
  f1=open('Lx_enclosed.dat','a')
  print ("%.6f	"%time, end="", file=f1)
  while m<len(r):
     sp=ds.sphere(c1,(r[m],'kpc'))
#     sp=ds.sphere(c1,(10,'kpc'))
     print ('sp=',sp)
#     mass = sum(sp["cell_mass"])
     total_xray_luminosity = sp['xray_luminosity_0.5_2_keV'].sum().in_units('erg/s')
     Lx.append(total_xray_luminosity)
     m=m+1
     print ("%.5e	"%total_xray_luminosity,end="", file =f1)
  print (" ",file=f1)
  f1.close()
     
  p = yt.ProjectionPlot(ds, 'x', "xray_emissivity_0.5_2_keV", width = (400,'kpc'))
  p.save()

num=[10,100,200,300,400,500]
num=range(220,600,30)
for i in num:
  see(i)
