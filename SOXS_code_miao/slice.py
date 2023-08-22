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

  c1 = [0.5,0.5,0.5]
  c1=[0,0,0]

  a1='grid_level'
  a1 = 'temperature'
  a1='number_density'
  a=[a1]
  pj_all = yt.SlicePlot(ds, 'x', a,center=c1, width=(100,'kpc'))
#  pj_all.set_zlim(a1,1,5)
  pj_all.save(a1+ '_' + str(i)+ '.png' )

yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

num = [202,300,330]
num=range(100,2000,100)
for i in num:
   see(i)

