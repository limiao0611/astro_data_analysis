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

def _metallicity(field,data):
    return data["SN_Colour"]/data["density"]

def _cool_rate(field,data):
    return data["cell_mass"]*data["GasEnergy"]/data["cooling_time"]

def _cool_time_inv(field,data):
    return 1./data["cooling_time"]

def _number_density(field,data):
    return abs(data['density']/YTQuantity(1.67e-24,'g'))



def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   a ='radius'
   b='temperature'
   c = "cell_mass"
   d=None

   c1= [0.5,0.5,0.5]
#   radius1 = YTQuantity(50,'kpc')
#   sphere1 = ds.sphere(c1, (50,'kpc'))

#   plot = PhasePlot(sphere1, a,b, [c],weight_field=d)
#   plot.save(a+ '_' + b+ '_' + c +'_' +str(i)+'.png')

#   shell1=sphere1.cut_region("obj['radius'].in_units('kpc')> 2.0   ")
   halo1 =  ad.cut_region(" obj['z']>0.53  ")
   plot = PhasePlot(halo1, a,b, [c],weight_field=d)
   plot.set_unit('radius','kpc')
   plot.save(a+ '_' + b+ '_' + c +'_' +str(i)+'_halo1.png')

   halo2 =  ad.cut_region(" obj['z']<0.47  ")
   plot = PhasePlot(halo2, a,b, [c],weight_field=d)
   plot.set_unit('radius','kpc')
   plot.save(a+ '_' + b+ '_' + c +'_' +str(i)+'_halo2.png')




yt.add_field('metallicity',function=_metallicity)
#yt.add_field('cool_rate',function=_cool_rate,units="erg/s")
yt.add_field('cool_time_inv',function=_cool_time_inv,units="1/s")
yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

num=[80,100,130]
num=range(100,3200,100)
for i in num:
    see(i)

