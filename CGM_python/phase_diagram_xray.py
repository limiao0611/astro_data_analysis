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


def _metallicity_solar(field,data):
    return data['metal_density']/data['density']/0.01295

def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   yt.add_xray_emissivity_field(ds, e_min=0.5,e_max= 2, metallicity = ("gas","metallicity_solar"), table_type = 'apec', cosmology =None)

   a='number_density'
#   b ='mass_flux_radial'
   b ='temperature'
   c='xray_emissivity_0.5_2_keV'
   d = "cell_volume"
#   d=None

   c1= [0.,0.,0.]
#   radius1 = YTQuantity(50,'kpc')
   sp = ds.sphere(c1, (50,'kpc'))

   plot = PhasePlot(sp,a,b,c,weight_field=d)
   plot.set_zlim(c, 1e-31,1e-27)
   plot.set_ylim(1e5,1e7)
   plot.save(a+'_'+b+'_'+c+'_50kpc_sphere_'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+d+'-weighted.png')

#yt.add_field('metallicity',function=_metallicity)
#yt.add_field('cool_rate',function=_cool_rate,units="erg/s")
yt.add_field('metallicity_solar',function=_metallicity_solar,units="")
yt.add_field('cool_time_inv',function=_cool_time_inv,units="1/s")
yt.add_field('vr',function=_vr, units  = 'km/s')
yt.add_field('mass_flux_radial',function=_mass_flux_radial, units  = 'msun/kpc**2/yr')
yt.add_field("energy_flux_radial",function=_energy_flux_radial,units='erg/kpc**2/yr')

num=range(1500,5000,500)
num=[300,500,1000,2000,3000,4000]
num=[0,10,20,30,40,50,60,70,80,100,200,300,400, 500]
for i in num:
    see(i)

