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
import gc

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

   c1= [0.,0.,0.]

   files = ['m_enclosed.dat', 'm_h_enclosed.dat', 'n_r_t.dat', 'P_r_t.dat']
#[10,20,30,40,50,60,80,100,120,160,200,240]
   r = [5,10,20,30,40,50,60,80,100,120,150,180,200,250,300,350,400]
   v=np.zeros(len(files))
   print ('v=',v)
   t = ds.current_time.in_units('Myr')
   for m in range(len(r)-1):
      sp1 = ds.sphere(c1, (r[m], 'kpc') )
      sp2 = ds.sphere(c1, (r[m+1], 'kpc'))
      v[0] =     m_enclosed = sp2['cell_mass'].sum().in_units('msun')

      hot_sp2 = sp2.cut_region("obj['temperature'].in_units('K')>3e4")
      v[1]= m_h_enclosed = hot_sp2['cell_mass'].sum().in_units('msun')

      shell = sp2- sp1 
      hot_shell = shell.cut_region("obj['temperature'].in_units('K')>3e4")
      v[2]= n_h_mean = hot_shell["number_density"].mean() #/YTQuantity(1,'1/cm**3')
#      print ("%5e	"%n_h_mean, end='')
#      print (" ")
      v[3] = P_h_mean = hot_shell["pressure"].mean().in_cgs()

      for k in range(len(files)):
          f=open(files[k],'a')
          if (m==0): print ("%5e	"%t, end='',file=f)
          print ("%5e	"%v[k], end='', file=f)
          f.close()
   for k in range(len(files)):
      f=open(files[k], 'a') 
      print ("	", file=f)
      f.close()

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
num=[0,10,50,70, 100,130,170,200,250,300,400,500,600,650,700,800]
num=[2,4,6,150,]
num=[1,3,5]
#num=[600,650,700,800]
#num=[1]
#num=range(220,380,30)
for i in num:
    see(i)

