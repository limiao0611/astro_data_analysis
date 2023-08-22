import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob

def _z_den_flux(field,data):
    return abs(data['density']*data['z-velocity'])
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')

def _ram_pressure(field,data):
    return data['density']* (data['z-velocity']*data['z-velocity']+ data['y-velocity']*data['y-velocity']+ data['x-velocity']*data['x-velocity'])

yt.add_field('ram_pressure',function=_ram_pressure, units  = 'dyne/cm**2')

ts=yt.load(glob.glob('DD*/sb_????'))
storage ={}
for sto, ds in ts.piter(storage=storage):

  fig = plt.figure()

  grid = AxesGrid(fig, (0.075,0.075,0.70,0.90), 
                nrows_ncols = (3,3),
                axes_pad = 1,
                label_mode = "1",
                share_all = True,
                cbar_location="right",
                cbar_mode="each",
                cbar_size="10%",
                cbar_pad="0%")

# fields = ['density','temperature','pressure','CREnergyDensity']
  fields = ['number_density','temperature','pressure','z-velocity','metallicity', 'ram_pressure' , 'entropy','cooling_time', 'mach_number']
  c = ['magma_r', 'plasma', 'arbre', 'bwr', 'YlGn', 'arbre', 'magma', 'magma', 'arbre']
  c1 = [0.00,0.00,0.0]
  p=yt.SlicePlot(ds,'x',fields,center=c1,axes_unit='kpc',fontsize=12, width=(400, 'kpc'))

  for m in range(len(fields)):
    p.set_cmap(fields[m], c[m] )
  p.set_log('z-velocity', False)
  p.set_log('metallicity', False)
  p.set_unit('z-velocity','km/s')
  p.set_unit('cooling_time','Gyr')
  p.set_zlim('number_density',1e-6, 1e-2)
  p.set_zlim('temperature',1e4,3e6)
  p.set_zlim('pressure',1e-16,1e-12)
  p.set_zlim('ram_pressure',1e-16,1e-12)
#  p.set_zlim('CREnergyDensity',1e-9,1e-2)
#  p.set_zlim('z_den_flux',1e-3,1.)
  p.set_zlim('z-velocity',-300,300)
  p.set_zlim('metallicity', 0.2,2)
  p.set_zlim('mach_number', 0.1,10)
  p.set_zlim('cooling_time', 0.1,20)
  p.set_zlim('entropy', 1,1e4)
  
  p.annotate_timestamp(corner='upper_left',time_unit='Myr',text_args={'color':'black'})

#  p.zoom(5)

  for j, field in enumerate(fields):
    plot = p.plots[field]
    plot.figure = fig
    plot.axes = grid[j].axes
    plot.cax = grid.cbar_axes[j]

  p._setup_plots()
  p.annotate_timestamp(corner='upper_left',time_unit='Myr',text_args={'color':'black'})
#  plt.title('t='+str(ds.current_time*ds.time_unit))
  plt.savefig('./x_slice1/multi_x_slice_'+str(ds)+'.png')
  sto.result_id=str(ds)

