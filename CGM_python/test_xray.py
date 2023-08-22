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
from yt import YTQuantity

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

def _metallicity_solar(field,data):
    return data['metal_density']/data['density']/0.01295

def see(i):
  fn = get_fn(i)
  ds = yt.load(fn)
  ad = ds.all_data()
  c1=[0.0, 0. ,0.]
  sp=ds.sphere(c1,(30,'kpc'))
  print ("metallicity=",(ad['metallicity']))
  print ("metallicity_solar=",(ad['metallicity_solar']))
#  print (YTQuantity(1,"Zsun").in_units(""))
#  yt.add_xray_emissivity_field(ds, 0.5, 1.5,with_metals=False,constant_metallicity=2.0 )
#  yt.add_xray_emissivity_field(ds, 0.5, 2 ,with_metals=True)

#  yt.add_xray_emissivity_field(ds, e_min=0.5,e_max= 2, metallicity = ("gas",'metallicity'), table_type = 'cloudy', cosmology =None)
#  yt.add_xray_emissivity_field(ds, e_min=0.3,e_max= 2, metallicity = ("gas",'metallicity'), table_type = 'apec', cosmology =None)
#  yt.add_xray_emissivity_field(ds, e_min=0.5,e_max= 2, metallicity = ("gas","metallicity_solar"), table_type = 'apec', cosmology =None)
  yt.add_xray_emissivity_field(ds, e_min=0.5,e_max= 2, metallicity = ("gas","metallicity_solar"), table_type = 'apec', cosmology =None)

  p = yt.ProjectionPlot(ds, 'x', "xray_emissivity_0.5_2_keV")
  p.save()

  time = ds.current_time.in_units("Gyr")
#  emission_per_cell = ad["xray_emissivity_0.5_2_keV"]* ad["cell_volume"]
#  total_xray_emission = sum(emission_per_cell.in_units("erg/s") )
  total_xray_luminosity = sum(sp['xray_luminosity_0.5_2_keV']).in_units('erg/s')
  f1=open('xray_emission_yt.dat','a')
#  print (time, total_xray_emission, total_xray_luminosity,file = f1)
  print (time, total_xray_luminosity,file = f1)
#  print (time, total_xray_emission,total_xray_luminosity)
  f1.close()

yt.add_field('metallicity_solar',function=_metallicity_solar,units="")
num=[10,100,200,300,400,500]
#num=[600,700,800]
for i in num:
  see(i)
