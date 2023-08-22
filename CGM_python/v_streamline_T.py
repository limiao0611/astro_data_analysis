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


### select your data file
ds = ts[i_file]
ds.periodicity = (False,False,False)
### create a sphere centered on your galaxy
sphere_out = ds.sphere([0.,0.,0.], (1.00*r200m.value, "kpc"))
sphere_in  = ds.sphere([0.,0.,0.], (0.10*r200m.value, "kpc"))
sphere = sphere_out - sphere_in
### TEMPERATURE with Line integral convolution
s = yt.SlicePlot(ds, 'x', 'temperature', data_source=sphere)
s.set_width((2.1*r200m.value, "kpc"))
s.set_zlim('temperature', 8e3, 1/0.8 * 1e6)
s.set_cmap('temperature', 'plasma')
s.annotate_line_integral_convolution('velocity_z', 'velocity_y',kernellen=30, lim=(0.4,0.65), alpha=0.6)
s.annotate_sphere([0, 0, 0], radius=(1.00*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
s.annotate_sphere([0, 0, 0], radius=(0.10*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
s.hide_axes(draw_frame=True)
s.hide_colorbar()
s.save('LIC', mpl_kwargs={'bbox_inches':'tight', 'dpi':400})
### TEMPERATURE with streamlines
s = yt.SlicePlot(ds, 'x', 'temperature', data_source=sphere)
s.set_width((2.1*r200m.value, "kpc"))
s.set_zlim('temperature', 8e3, 1/0.8 * 1e6)
s.set_cmap('temperature', 'plasma')
s.annotate_streamlines('velocity_z', 'velocity_y', field_color='velocity_magnitude', display_threshold=0.1, factor=8, density=4)
s.annotate_sphere([0, 0, 0], radius=(1.00*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':20})
s.annotate_sphere([0, 0, 0], radius=(0.10*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
s.hide_axes(draw_frame=True)
s.hide_colorbar()
s.save('stream', mpl_kwargs={'bbox_inches':'tight', 'dpi':400})
### DENSITY with LIC 
s = yt.SlicePlot(ds, 'x', 'density', data_source=sphere)
s.set_width((2.1*r200m.value, "kpc"))
s.set_zlim('density', 3e-30, 3e-27)
s.annotate_line_integral_convolution('velocity_z', 'velocity_y', lim=(0.5,0.65))
s.annotate_sphere([0, 0, 0], radius=(1.00*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
s.annotate_sphere([0, 0, 0], radius=(0.10*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
s.hide_axes(draw_frame=True)
s.hide_colorbar()
s.save(mpl_kwargs={'bbox_inches':'tight', 'dpi':400})


