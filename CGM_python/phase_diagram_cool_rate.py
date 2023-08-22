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

def ReadCoolingCurve():
    FileIn = open("cool_rates.in")
    data = loadtxt(FileIn)
    FileIn.close()
    return (data[:,0],data[:,2])

(LogT, LogCoolRate) = ReadCoolingCurve()

def _cooling_rate(field,data):
    return 10.0**interp(log10(data["temperature"]), LogT, LogCoolRate)* YTQuantity(1,"erg*cm**3/s")

m_H = YTQuantity(1.67e-24,'g')
mu = 0.6*m_H
def _cooling_rate_per_volume(field,data):
    return 1.76*0.4* data["cooling_rate"] *data["density"]**2/m_H/mu

def _cooling_rate_per_cell(field,data):
    return data["cooling_rate_per_volume"]*data["cell_volume"]


def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   a ='density'
   b='temperature'
   c = "cooling_rate_per_cell"
   d=None

   c1= [0.,0.,0.]
   radius1 = YTQuantity(50,'kpc')
   sphere1 = ds.sphere(c1, (200,'kpc'))

#   plot = PhasePlot(sphere1, a,b, [c],weight_field=d)
#   plot.save(a+ '_' + b+ '_' + c +'_' +str(i)+'.png')

   shell1=sphere1.cut_region("obj['radius'].in_units('kpc')> 25.0")

   sphere1_hot = sphere1.cut_region("obj['temperature']>2e6")

   plot = PhasePlot(sphere1_hot, a,b, [c],weight_field=d)
   plot.save(a+ '_' + b+ '_' + c +'_' +str(i)+'_sphere_hotter_than_2e6k.png')
   time = ds.current_time.in_units("Gyr")
   cool_rate_hot_gas =sum(sphere1_hot["cooling_rate_per_cell"])
   f1=open("cool_rate_hot_gas.dat",'a')
   print (time, cool_rate_hot_gas,file=f1)
   f1.close()

#   hot = ad.cut_region("obj['temperature']>3e4")
#   midplane = ad.cut_region("obj['z']<0.1 and obj['z']>-0.1")
#   midplane = ad.cut_region("obj['z']<0.1") and ad.cut_region("obj['z']>-0.1")

#   midplane = ds.box([0,0,-0.1],[0.24,0.24,0.1])
#   halo = ad.cut_region("obj['z']>0.2") and ad.cut_region("obj['z']<-0.2")

#   plot = PhasePlot(ad,a,b ,[c] ,weight_field=d)
#   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+d+'-weighted.png')

#   plot = PhasePlot(midplane,a,b,c,weight_field=d)
#   plot.save(a+'_'+b+'_'+c+'_midplane1_'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'_midplane1_'+str(i)+d+'-weighted.png')

#   plot = PhasePlot(halo,a,b,c,weight_field=d)
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+d+'-weighted.png')

yt.add_field('metallicity',function=_metallicity)
#yt.add_field('cool_rate',function=_cool_rate,units="erg/s")
yt.add_field('cool_time_inv',function=_cool_time_inv,units="1/s")
yt.add_field('cooling_rate',function=_cooling_rate,units="erg*cm**3/s")
yt.add_field('cooling_rate_per_volume',function=_cooling_rate_per_volume,units="erg/cm**3/s")
yt.add_field('cooling_rate_per_cell',function=_cooling_rate_per_cell,units="erg/s")

num=[80,100,130]
num=range(300,5000,1000)
num=[300,500,1000,2000,3000,4000]
for i in num:
    see(i)

