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
  shell1=sphere1.cut_region("obj['radius'].in_units('kpc')> 15.0")

  a = ["radius"]
  b = ["SN_Colour"]

  profiles.append(yt.create_profile(shell1, a,fields=b) )
  time = (ds.current_time).in_units('Gyr')

  labels.append("t = %.1f Gyr" % time)
  plot_specs.append(dict(linewidth=2, alpha=0.7))

  a0.append(a[0])
  b0.append(b[0])


yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

num=[20,100,200,300,400,500]
num=[20,100,200,300,380]
num=[30,60,90,120,150,180,220]
num=[20,100,300,600,900]
for i in num:
   see(i)
   print (a0[0])

plot = yt.ProfilePlot.from_profiles(profiles, labels=labels,
                                 plot_specs=plot_specs)
plot.set_unit('radius', 'kpc')
plot.set_ylim("SN_Colour",1e2,1e8)
# Save the image.
plot.save(a0[0]+"_"+b0[0]+"_t_"+str(num)+"_1.png")


