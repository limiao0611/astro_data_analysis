import yt
from yt import *
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

def _vz_abs(field,data):
    return abs(data['z-velocity'])

def see(i):
  fn = get_fn(i)

  ds = yt.load(fn)

  c1 = [0.5,0.5,0.5]
  #c1=[0.545,0.599,0.602]
  #c1 =[0.891576, 0.130623, 0.186343]
#  sp=ds.sphere(c1, (20, 'pc'))

  ad=ds.all_data()
#  print ad['gas','density']
#  print 'min_den=', min(ad['gas','density'])
#  print ad['enzo','Temperature']
#  print ad['enzo','z-velocity']
#  low = abs(ad['index','z'])<0.003
#  print 'density at low altitude=',ad['gas','density'][low]
#  print 'z-vel at low altitude=',ad['enzo','z-velocity'][low]
#  print 'temp at low altitude=',ad['enzo','Temperature'][low]
#  high = ad['index','z']>0.48
#  print 'density at high altitude=',ad['gas','density'][high]
#  print 'temp at high altitude=',ad['enzo','Temperature'][high]
#  print 'sum den=',sum(ad['gas','density']) 

#  cool=ad.cut_region("obj['temperature']<3e4")
#  cool_high = cool.cut_region("obj['z']>0.53 ")
  cool_high_vz_plus = ad.cut_region(" (obj['temperature']<3e4)  & (obj['z']>0.53)  & (obj['z-velocity']>0  ) ")
  cool_high_vz_minus = ad.cut_region(" (obj['temperature']<3e4)  & (obj['z']>0.53)  & (obj['z-velocity']<0  ) ")
#  print (cool_high['z-velocity'].in_units('km/s') )
  print (cool_high_vz_plus['z'] )
  plot = ProfilePlot(cool_high_vz_plus,'z-velocity','cell_mass',weight_field=None)
  plot.set_unit('z-velocity','km/s')
  plot.save('cool_high_vz_plus-'+str(i)+'.png')

  plot = ProfilePlot(cool_high_vz_minus,'vz_abs','cell_mass',weight_field=None)
  plot.save('cool_high_vz_minus-'+str(i)+'.png')

#  field ='velocity'
#  weight='cell_mass'
#  v_cool_high = (cool_high.quantities.weighted_average_quantity(field,weight)).in_units('km/s')
#  field='z-velocity'
#  vz_cool_high = (cool_high.quantities.weighted_average_quantity(field,weight)).in_units('km/s')
   
#  print ("v_cool_high=",v_cool_high)
#  print ("vz_cool_high=",vz_cool_high)

yt.add_field('vz_abs',function=_vz_abs, units  = 'km/s')
num =[1,10,100,580]
num = [1500,1800,1100,900]

for i in num:
   see(i)


