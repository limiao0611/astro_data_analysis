import matplotlib
from numpy import *
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
yt.enable_parallelism()
import matplotlib.pyplot as plt

def get_fn(i):
    a0=''
    if (i<10):
      a0='000'
    if (10<=i<100):
      a0='00'
    if (100<=i<=999):
      a0='0'
    filen='DD'+a0+str(i)+'/sb_'+a0+str(i)
    return filen

def _z_den_flux(field,data):
    return abs(data['density']*data['z-velocity'])

def _CR_Energy_Density(field,data):
    return data['CREnergyDensity']* data.ds.mass_unit/data.ds.length_unit/data.ds.time_unit**2

def _vr(field,data):
   center = data.ds.domain_center
   location_vector = [data['x']-center[0], data['y']-center[1], data['z']-center[2]]
   vr =  data['x-velocity'] * (data['x']-center[0]) +  data['y-velocity'] * (data['y']-center[1])+  data['z-velocity'] * (data['z']-center[2])
   vr = vr/sqrt((data['x']-center[0])**2 + (data['y']-center[1])**2+ (data['z']-center[2])**2)
   return vr


def _mass_flux_radial(field,data):
   return abs(data['density']* data['vr'])

def _total_mass_flux_radial(field,data):
   center = data.ds.domain_center
   radius = sqrt((data['x']-center[0])**2 + (data['y']-center[1])**2+ (data['z']-center[2])**2)
   return data['density']* data['vr']* 4*3.1415926535* radius**2

def _total_energy_flux_radial(field,data):
   center = data.ds.domain_center
   radius = sqrt((data['x']-center[0])**2 + (data['y']-center[1])**2+ (data['z']-center[2])**2)
#   specific_energy_unit = data.ds.length_unit**2/data.ds.time_unit**2
   specific_energy_unit = 1.
   return data['density']* data["TotalEnergy"] *data["vr"] * specific_energy_unit *  4*3.1415926535* radius**2



def _momentum_flux_radial(field,data):
   return data['density']* data['vr']**2 # * sign(data['vr'])

def _number_density(field,data):
    return abs(data['density']/YTQuantity(1.67e-24,'g'))

profiles = []
labels = []
plot_specs = []
a0=[]
b0=[]

def see(i):
  fn = get_fn(i)
  ds = yt.load(fn)

#  ad=ds.all_data()
  c1= [0.,0.,0.]
  sphere1 = ds.sphere(c1, (300,'kpc'))
  shell1=sphere1.cut_region("obj['radius'].in_units('kpc')> 10.0")
#  out=shell1.cut_region("obj['vr']>0.0")
  out = sphere1.cut_region(" (obj['radius'].in_units('kpc')> 10.0)  &  (obj['vr']>0.0)   ")

  a = "radius"
  b = "total_mass_flux_radial"
  c="cell_volume"
  nbin=20
  pro1 = yt.create_profile(out, a,fields=b, weight_field = c, n_bins=nbin, logs=None, units={'radius':'kpc'}, extrema={'radius': (10,300)} )
  pro2 = yt.create_profile(shell1, a, fields = "cell_volume", weight_field = None, n_bins=nbin, logs=None, units={'radius':'kpc'}, extrema={'radius': (10,300)})
  pro3 = yt.create_profile(out, a, fields = "cell_volume", weight_field = None, n_bins=nbin, logs=None, units={'radius':'kpc'}, extrema={'radius': (10,300)})
  print ("pro1=",pro1.x.shape)
  print ("pro1=",pro1.x)
  print ("pro1.x/pro2.x=",pro1.x/pro2.x)
  print ("pro1.x/pro3.x=",pro1.x/pro3.x)
  print ("pro1=",pro1.x.value)
  print ("fractional_volume=", pro3['cell_volume']/pro2['cell_volume'] )
#  print ("pro1 y=",pro1['total_energy_flux_radial'].value)
#  print ("pro1 y=",pro1['total_energy_flux_radial'] * pro3['cell_volume']/pro2['cell_volume'] )
#  print ("pro1 y=",pro1['total_energy_flux_radial'])
  x = pro1.x.in_units("kpc")
  y = pro1[b] * (pro3['cell_volume']/pro2['cell_volume'])
#  print ("after pro1 y=",pro1['total_energy_flux_radial'])
  print ("x=",x)
  print ("y=",y)
#  profiles.append(pro1)
  time = (ds.current_time).in_units('Gyr')
  plt.plot(x,y, label="t = %.1f Gyr" % time)
  
#  labels.append("t = %.1f Gyr" % time)
#  plot_specs.append(dict(linewidth=2, alpha=0.7))

  a0.append(a[0])
  b0.append(b[0])

yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
yt.add_field('vr',function=_vr, units  = 'km/s')
yt.add_field('number_density',function=_number_density, units  = '1/cm**3')
yt.add_field('mass_flux_radial',function=_mass_flux_radial, units  = 'msun/kpc**2/yr')
yt.add_field('total_mass_flux_radial',function=_total_mass_flux_radial, units  = 'msun/yr')
#yt.add_field('momentum_flux_radial',function=_momentum_flux_radial, units  = 'msun/kpc/yr**2')
yt.add_field('momentum_flux_radial',function=_momentum_flux_radial, units  = 'dyne/cm**2')
yt.add_field('total_energy_flux_radial',function=_total_energy_flux_radial, units  = 'erg/yr')

num=[20,100,200,300,400,500]
num=[20,100,200,300,400]
num=[1,10,30,50,95]
num=[5,10,15,20,26]
num=[30,60,90,120,150,180,210]
num=[20,100,300,600,900]
num=[20,60,100,200,300,400,500,600]
num =range(10,800,50)
#num =[1, 20, 60,100,140]
#num=[320,322,324,326,328,330,332,334]
#num=[20,22,24,26,28,30,32,34]
for i in num:
   see(i)
   print (a0[0])

plt.xscale('log')
plt.yscale('log')
plt.ylim(1e-1, 10)
plt.xlabel('r [kpc]')
plt.ylabel('total mass flux [Msun/yr]')
plt.legend(loc=1)
plt.savefig("total_mass_flux_outgoing_t_"+str(num)+"_min10kpc.png")
#plot = yt.ProfilePlot.from_profiles(profiles, labels=labels,
#                                 plot_specs=plot_specs)
#plot.set_unit('radius', 'kpc')
# Save the image.
#plot.save(a0[0]+"_"+b0[0]+"_outgoing_t_"+str(num)+"_1.png")


