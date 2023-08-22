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


def _cool_rate(field,data):
    return data["cell_mass"]*data["GasEnergy"]/data["cooling_time"]

def _cool_time_inv(field,data):
    return 1./data["cooling_time"]

def _vr(field,data):
   center = data.ds.domain_center
   location_vector = [data['x']-center[0], data['y']-center[1], data['z']-center[2]]
   vr =  data['x-velocity'] * (data['x']-center[0]) +  data['y-velocity'] * (data['y']-center[1])+  data['z-velocity'] * (data['z']-center[2])
   vr = vr/sqrt((data['x']-center[0])**2 + (data['y']-center[1])**2+ (data['z']-center[2])**2)
   return vr


def _mass_flux_radial(field,data):
   return abs(data['density']* data['vr'])

def _energy_flux_radial(field,data):
#   return abs(data['density']* (0.5*data['vr']**2 + data["GasEnergy"])*data["vr"]   )   
   specific_energy_unit = data.ds.length_unit**2/data.ds.time_unit**2
   return abs(data['density']* data["TotalEnergy"] *data["vr"]   )*specific_energy_unit   

def _cell_etot(field, data):
    return data['cell_mass']*data['TotalEnergy']

def _cell_eth(field, data):
    return data['cell_mass']*data['GasEnergy']


def _cell_ek(field, data):
    return data['cell_etot'] - data['cell_eth']

def _cell_cool_rate(field, data):
    return data['cell_eth']/data['cooling_time']

def _cell_metal_mass(field, data):
    return data['metal_density']*data['cell_volume']



def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()


   c1= [0.,0.,0.]
   sp = ds.sphere(c1, (100,'kpc'))


   mass = sum(sp['cell_mass']).in_units('msun')
#   hot = sp.cut_region("obj['temperature'] > 1. ") 
   hot = sp['temperature'].in_units('K') > 3e4
   wh = (sp['temperature'].in_units('K') < 3e4) & (sp['temperature'].in_units('K') > 1e3)
   cool = sp['temperature'].in_units('K') < 1e3
#   sp1 = ad.cut_region("obj[radius]")
   mass_hot = sum(sp['cell_mass'][hot]).in_units('msun')
   mass_wh= sum(sp['cell_mass'][wh]).in_units('msun')
   mass_cool = sum(sp['cell_mass'][cool]).in_units('msun')

   cool_rate_h = sum(sp['cool_rate'][hot])
   cool_rate_wh = sum(sp['cool_rate'][wh])
   cool_rate_c = sum(sp['cool_rate'][cool])

   time = ds.current_time.in_units('Gyr')
   print ("t, mass, mass_hot, mass_wh, mass_cool=%f, %e, %e, %e   %e"%(time, mass, mass_hot, mass_wh, mass_cool) )
   f1 =open('cool_phase_newdef1.dat','a')
   print ("t(Gyr), mass, mass_hot, mass_wh, mass_cool, cool_rate_hot, wh, c=%f, %e, %e,  %e,  %e, %e, %e,  %e  "%(time,mass, mass_hot, mass_wh,  mass_cool, cool_rate_h, cool_rate_wh, cool_rate_c) , file =f1)
   f1.close()

yt.add_field('cool_rate',function=_cool_rate,units="erg/s")
yt.add_field('cool_time_inv',function=_cool_time_inv,units="1/s")
yt.add_field('vr',function=_vr, units  = 'km/s')
yt.add_field('mass_flux_radial',function=_mass_flux_radial, units  = 'msun/kpc**2/yr')
yt.add_field("energy_flux_radial",function=_energy_flux_radial,units='erg/kpc**2/yr')
yt.add_field('cell_etot',function = _cell_etot, units='erg')
yt.add_field('cell_eth',function = _cell_eth, units='erg')
yt.add_field('cell_ek',function = _cell_ek, units='erg')
yt.add_field('cell_cool_rate',function=_cell_cool_rate, units='erg/yr')
yt.add_field('cell_metal_mass', function=_cell_metal_mass, units='Msun')

num=range(1500,5000,500)
num=[300,500,1000,2000,3000,4000]
num=range(50,650,100)
num=[10,20,30,40,50,100,200,300,400,500]
num=range(10,800,30)
#num=range(60,100,10)
for i in num:
    see(i)

