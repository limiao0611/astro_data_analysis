import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
#yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

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



def see(i):
  fn = get_fn(i)

  ds = yt.load(fn)
  ad = ds.all_data()

  c1 = [0.,0.,0.]

  cool = ad.cut_region('obj["temperature"]<3e4')
  a1='number_density'
  a=[a1]
  pj_all = yt.ProjectionPlot(ds, 'x', a,center=c1,weight_field=None, data_source=cool, width=(150,'kpc'), fontsize=25)
  pj_all.annotate_timestamp(corner='upper_left',time_unit='Gyr',text_args={'color':'black'})
  pj_all.set_zlim(a1, 1e18, 1e21 )
  pj_all.save('projection_' + a1+ '_' + str(i)+ '_cool_R150kpc.png' )


yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

num = range(40,930)
num=[300,320, 340]
for i in num:
   see(i)

