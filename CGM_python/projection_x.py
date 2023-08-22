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
  #c1=[0.545,0.599,0.602]
  #c1 =[0.891576, 0.130623, 0.186343]
#  sp=ds.sphere(c1, (1, 'kpc'))

#  slc = yt.ProjectionPlot(ds, 'x', ['z-velocity'],center=c1,weight_field='density').annotate_grids()
#  slc.save()
#  slc = yt.ProjectionPlot(ds, 'x', ['TotalEnergy'],center=c1,weight_field='density').annotate_grids()
#  slc.save()

#  slc = yt.ProjectionPlot(ds, 'x', ['number_density'],center=c1,weight_field=None)
#  slc.save()

#  slc = yt.ProjectionPlot(ds, 'y', ['density'],center=c1,weight_field=None)
#  slc.set_unit('density','msun/pc**2')
#  slc.save()

#  slc = yt.ProjectionPlot(ds, 'z', ['density'],center=c1,weight_field=None)
#  slc.set_unit('density','msun/pc**2')
#  slc.save()

  a1='number_density'
  a2='metal_density'
  a3 ='pressure'
  a=[a1,a2, a3]
  pj_all = yt.ProjectionPlot(ds, 'x', a,center=c1,weight_field=None)
#  pj_all.save('projection_' + a1+ '_' + str(i)+ '_all.png' )
  pj_all.save()

yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

num = [1,10,30,50,70,90,100]
num=[10,30,50,100,150,200,300,400,500]
for i in num:
   see(i)

