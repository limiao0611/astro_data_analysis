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
from yt.utilities.physical_constants import *
from yt.units import *

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

def see(i):
    OL = 0.73
    Om = 0.27

    H0 = 70 * km /second / Mpc
    mu = 0.62
    muH = 1/0.7
    Tcool =1e4
    M15=1e-3
    zz=0
   
    F17_color='grey'

    Tcool *= K
    UnitLength = YTQuantity((G * M15 * 1e15 * Msun / H0**2)**(1./3.)).convert_to_units('kpc')
#    UnitTime = YTQuantity(1/H0).convert_to_units('yr')
#    UnitMass = YTQuantity(M15 * 1e15 * Msun).convert_to_units('Msun')
#    UnitTemp = 4.688*0.62*M15**(2./3.) *keV
#    kbTfloor = Tigm*UnitTemp
    H = np.sqrt(OL + (1+zz)**3 * Om)
    r200m = UnitLength * (H**2/( (1+zz)**3 * Om))**(1./3.)*(10*H)**(-2./3.)
#    r200m = 200.
### select your data file
    fn = get_fn(i)
    ds = yt.load(fn)
#    ds = ts[i_file]
#    ds.periodicity = (False,False,False)
### create a sphere centered on your galaxy
    sphere_out = ds.sphere([0.,0.,0.], (1.00*r200m.value, "kpc"))
    sphere_in  = ds.sphere([0.,0.,0.], (0.10*r200m.value, "kpc"))
    sphere = sphere_out - sphere_in
### TEMPERATURE with Line integral convolution
    s = yt.SlicePlot(ds, 'x', 'temperature')#, data_source=sphere)
    s.set_width((1.0*r200m.value, "kpc"))
#    s.set_width((2.1*r200m.value, "kpc"))
    s.set_zlim('temperature', 8e3, 1/0.8 * 1e6)
    s.set_cmap('temperature', 'plasma')
    ad=ds.all_data()
    print(sphere['z-velocity'])
    print(sphere['y-velocity'])
    s.annotate_line_integral_convolution('y-velocity', 'z-velocity', lim=(0,1))#,kernellen=30, lim=(0.4,0.65), alpha=0.6, )
    s.annotate_sphere([0, 0, 0], radius=(1.00*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
    s.annotate_sphere([0, 0, 0], radius=(0.10*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
    s.hide_axes(draw_frame=True)
#    s.hide_colorbar()
    s.save('LIC'+str(i), mpl_kwargs={'bbox_inches':'tight', 'dpi':400})
### TEMPERATURE with streamlines
    s = yt.SlicePlot(ds, 'x', 'temperature')#, data_source=sphere)
    s.set_width((2.1*r200m.value, "kpc"))
    s.set_zlim('temperature', 8e3, 1/0.8 * 1e6)
    s.set_cmap('temperature', 'plasma')
#    s.annotate_streamlines('velocity_z', 'velocity_y', field_color='velocity_magnitude', display_threshold=0.1, factor=8, density=4)
    s.annotate_streamlines('y-velocity', 'z-velocity',field_color='velocity_magnitude',factor=16, density=10)#, field_color=None, display_threshold=0.1, factor=8, density=4)
    s.annotate_sphere([0, 0, 0], radius=(1.00*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':20})
    s.annotate_sphere([0, 0, 0], radius=(0.10*r200m.value, "kpc"),
              circle_args={'color':F17_color, 'linewidth':5})
    s.hide_axes(draw_frame=True)
#    s.hide_colorbar()
    s.save('stream_'+str(i), mpl_kwargs={'bbox_inches':'tight', 'dpi':400})

num=[301]
for i in num:
    see(i)
