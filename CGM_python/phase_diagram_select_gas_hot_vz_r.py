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

def _velocity(field,data):
   v =sqrt (data['x-velocity'] * data['x-velocity']  + data['y-velocity'] *data['y-velocity'] + data['z-velocity']* data['z-velocity'])
   return v



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
   sphere1 = ds.sphere(c1, (10,'kpc'))
   sphere2 = ds.sphere(c1, (400,'kpc'))
#   shell1=sphere1.cut_region("obj['radius'].in_units('kpc')> 10.0")
#   shell1_out = shell1.cut_region("obj['metallicity'].in_units('solar_metallicity')> 0.5 ")
#   out = ad.cut_region("obj['metallicity']> 0.5 ")
#   out = ad.cut_region("obj['metallicity'].in_units('solar_metallicity')> 0.5 ")
#   cool = ad.cut_region("obj['temperature']< 3e4 ")

#   hot = ad.cut_region("obj['temperature']> 3e4 ")
   
#   hot = ad-cool
#   hot_enrich =  hot.cut_region("obj['metallicity'].in_units('Zsun')> 0.4 ")
   cgm = sphere2-sphere1
   hot = cgm.cut_region("obj['temperature']> 3e4 ")
#   cool = cgm.cut_region("obj['temperature']< 3e4 ")

   a = 'radius'
#   b='temperature'
#   a='number_density'
#   b ='mass_flux_radial'
#   a='temperature'
#   b ='metallicity'
   b='z-velocity'
   
#   b='velocity'
#   b ='mach_number'
#   b = 'cooling_time'
#   b='entropy'
#   b='x-velocity'
#   b="number_density"
#   b='metallicity'
   c = "cell_mass"
   d=None
 #   d='cell_volume'


   plot = PhasePlot(hot,a,b,c,weight_field=d)
   plot.set_unit('radius','kpc')
#   plot.set_unit(b,'Gyr')
#   plot.set_unit('cell_mass','msun')
#   plot.set_unit('radial_velocity','km/s')
#   plot.set_unit('velocity','km/s')
   plot.set_unit('z-velocity','km/s')
#   plot.set_log('radial_velocity',0)
#   plot.set_log('velocity',0)
   plot.set_log('z-velocity',0)
   plot.set_ylim(-400,400)
   plot.set_xlim(10,400)
#   plot.set_zlim(c, 1e3, 1e7)
   plot.set_cmap("cell_mass", "YlOrBr")
   plot.save(a+'_'+b+'_'+c  +str(i)+'_hot.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+d+'-weighted.png')

#yt.add_field('cool_rate',function=_cool_rate,units="erg/s")
yt.add_field('cool_time_inv',function=_cool_time_inv,units="1/s")
yt.add_field('vr',function=_vr, units  = 'km/s')
yt.add_field('velocity',function=_velocity, units  = 'km/s')
yt.add_field('mass_flux_radial',function=_mass_flux_radial, units  = 'msun/kpc**2/yr')
yt.add_field("energy_flux_radial",function=_energy_flux_radial,units='erg/kpc**2/yr')
yt.add_field('cell_etot',function = _cell_etot, units='erg')
yt.add_field('cell_eth',function = _cell_eth, units='erg')
yt.add_field('cell_ek',function = _cell_ek, units='erg')
yt.add_field('cell_cool_rate',function=_cell_cool_rate, units='erg/yr')
yt.add_field('cell_metal_mass', function=_cell_metal_mass, units='Msun')

num=range(300,450,10) 
num=[300, 400, 500]
num=[200,250, 300,400,500]
#num=[0]
for i in num:
    see(i)

