import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
import mpi4py

def _number_density(field,data):
    return abs(data['density']/YTQuantity(1.67e-24,'g'))

yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

ts=yt.load(glob.glob('DD*/sb_????'))
storage ={}
for sto, ds in ts.piter(storage=storage):
  fig = plt.figure()
  c1 = [0.,0.,0.]
  ad = ds.all_data()
  cool = ad.cut_region('obj["temperature"]<3e4')
  cool1 = cool.cut_region('obj["radius"].in_units("kpc")<100')  

  a1='number_density'
  a=[a1]
  
  pj_all = yt.ProjectionPlot(ds, 'x', a,center=c1,weight_field=None, data_source=cool1, width=(200,'kpc'))
  pj_all.set_zlim(a1, 1e19, 1e23 )
  pj_all.annotate_timestamp(corner='upper_left',time_unit='Myr',text_args={'color':'black'})
  pj_all.save('./proj_cool/projection_' + a1+ '_' + str(ds)+ '_cool_260kpc.png' )

  sto.result_id=str(ds)  



