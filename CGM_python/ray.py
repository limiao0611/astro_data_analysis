import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
#yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

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



def see(i):
  fn = get_fn(i)

  ds = yt.load(fn)
  ad = ds.all_data()

  c1 = [0.0,0.,0.]
  
#  start =( (0.5, "kpc"), (0.5, "kpc"), (0.5,"kpc") )
#  end = ( (2, "kpc"), (2, "kpc"), (2,"kpc") )
#  ray1= ds.r[start:end] 
  start = ((0.0, "kpc"), (0.0, "kpc"), (0.0, "kpc"))
  end = ((0.0, "kpc"), (300.0, "kpc"), (300.0, "kpc"))
  ray = ds.r[start:end]

  field = 'number_density'
  plot = yt.ProfilePlot(ray, 'radius', field)
  plot.set_unit('radius','kpc')
  plot.save() 

yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

num = [202,300,330]
num=[1,50,100]
for i in num:
   see(i)

