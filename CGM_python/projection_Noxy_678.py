import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
#yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from numpy import *
from scipy.interpolate import interp1d

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


yt.add_field('number_density',function=_number_density, units  = '1/cm**3')

T_fit=array(           [0.0, 5.0,  5.05,  5.20,   5.40,    5.45,  5.90 , 6.35,   7.15  , 7.5,  12. ])
fOVI_log10_fit = array( [100., 10., 6.099, 3.070,  0.801,  0.657,  2.254, 2.826,  6.891, 10,   100. ] )
f_linear=interp1d(T_fit, fOVI_log10_fit)

def OVI_fraction(T):
    return pow(10,-f_linear(log10(T) ))


def _f_OVI(field,data):
    return OVI_fraction(data['temperature'])

yt.add_field('f_OVI',function=_f_OVI,units='')

def _n_OVI(field,data):
     f_O = 5e-4 # Oxygen: fraction of number density for gas with solar metallicity
     n_e =  data['number_density']*11./13
     n_H = n_e * 9./11
     return n_H * data['metallicity']/YTQuantity(1.0,'Zsun') * f_O * data['f_OVI']

yt.add_field('n_OVI',function=_n_OVI, units  = '1/cm**3')


################
f=open('oxygen_ion_abundance.dat','r')
T_log, fo6_log, fo7_log, fo8_log = loadtxt(f, usecols=(0,1,2,3), unpack=True)
f.close()

f_lin6 = interp1d(T_log, fo6_log)
f_lin7 = interp1d(T_log, fo7_log)
f_lin8 = interp1d(T_log, fo8_log)

def _f_o6(field,data):
    return pow(10, f_lin6(log10(data['temperature']))  )
yt.add_field('f_o6', function=_f_o6, units='')

def _n_O6(field,data):
     f_O = 5e-4 # Oxygen: fraction of number density for gas with solar metallicity
     n_e =  data['number_density']*11./13
     n_H = n_e * 9./11
     return n_H * data['metallicity']/YTQuantity(1.0,'Zsun') * f_O * data['f_o6']

yt.add_field('n_O6',function=_n_O6, units  = '1/cm**3')

###
def _f_o7(field,data):
    return pow(10, f_lin7(log10(data['temperature']))  )
yt.add_field('f_o7', function=_f_o7, units='')

def _n_O7(field,data):
     f_O = 5e-4 # Oxygen: fraction of number density for gas with solar metallicity
     n_e =  data['number_density']*11./13
     n_H = n_e * 9./11
     return n_H * data['metallicity']/YTQuantity(1.0,'Zsun') * f_O * data['f_o7']

yt.add_field('n_O7',function=_n_O7, units  = '1/cm**3')
###

def _f_o8(field,data):
    return pow(10, f_lin8(log10(data['temperature']))  )
yt.add_field('f_o8', function=_f_o8, units='')

def _n_O8(field,data):
     f_O = 5e-4 # Oxygen: fraction of number density for gas with solar metallicity
     n_e =  data['number_density']*11./13
     n_H = n_e * 9./11
     return n_H * data['metallicity']/YTQuantity(1.0,'Zsun') * f_O * data['f_o8']

yt.add_field('n_O8',function=_n_O8, units  = '1/cm**3')


###########


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

#  hot_x = ad.cut_region('obj["temperature"].in_units("K")> 5e5')
  a1='n_O6'
  a2='n_O7'
  a3='n_O8'
  a=[a1, a2, a3]
  pj_all = yt.ProjectionPlot(ds, 'x', a,center=c1,weight_field=None, width = (500,'kpc'))
  pj_all.set_zlim(a1, 1e13, 3e15 )
  pj_all.set_zlim(a2, 1e13, 3e17 )
  pj_all.set_zlim(a3, 1e13, 3e17 )
  pj_all.save()
#  pj_all.save('projection_' + a1+ '_' + str(i)+ '_Mazzotta98.png' )
  


num = [100,200,300,400,500,550,600,630,650,675, 700,730,750]
num=range(280,306,2)
for i in num:
   see(i)

