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

def _polar_angle(field,data):
    return abs(data['z']/data['radius'])

def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   a='radius'
#   b ='mass_flux_radial'
#   b ='entropy'
#   b="number_density"
   b='polar_angle'
   c = "metallicity"
   d="cell_volume"

   c1= [0.,0.,0.]

   logs={b:False, c: False}
   units = {a: 'kpc', c: 'Zsun'}
   extrema = {a: (5,400), b: (0.0,1.0)  ,c :(0.2,4)}
   prof = yt.create_profile(ad, [a,b],fields=c,logs=logs, weight_field=d, extrema=extrema, units=units, n_bins =[128,30] )
   fn = prof.save_as_dataset(a+'_'+b+'_'+c+str(i)+".dat")
   plot = PhasePlot.from_profile(prof)
#   plot.set_unit('radius','kpc')
   plot.set_log(b, False)
   plot.set_log(c, False)
   plot.set_xlim(10,400)
   plot.set_ylim(-0.1,1.1)
   plot.set_zlim(c,0.2,4)
   plot.set_cmap(c,"magma_r")
   plot.save(a+'_'+b+'_'+c+'all'+str(i)+'_create_profile.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+d+'-weighted.png')

#yt.add_field('cool_rate',function=_cool_rate,units="erg/s")
yt.add_field('cool_time_inv',function=_cool_time_inv,units="1/s")
yt.add_field('vr',function=_vr, units  = 'km/s')
yt.add_field('mass_flux_radial',function=_mass_flux_radial, units  = 'msun/kpc**2/yr')
yt.add_field("energy_flux_radial",function=_energy_flux_radial,units='erg/kpc**2/yr')
yt.add_field('cell_etot',function = _cell_etot, units='erg')
yt.add_field('cell_eth',function = _cell_eth, units='erg')
yt.add_field('cell_ek',function = _cell_ek, units='erg')
yt.add_field('cell_cool_rate',function=_cell_cool_rate, units='erg/yr')
yt.add_field('cell_metal_mass', function=_cell_metal_mass, units='Msun')
yt.add_field('polar_angle',function = _polar_angle, units='')

num=range(1500,5000,500)
num=[300,500,1000,2000,3000,4000]
num=range(50,650,100)
num=[10,50,70, 100,130,170,200,250,300,400,500, 600,700,800]
#num=range(220,380,30)
for i in num:
    see(i)

