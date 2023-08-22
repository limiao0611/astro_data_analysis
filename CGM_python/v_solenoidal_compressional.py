import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
#yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from numpy import *
from numpy.fft import *
from scipy import stats

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
    print ('data1.shape=',data['density'].shape)
    return abs(data['density']/YTQuantity(1.67e-24,'g'))


def _phi_v(field,data):
#  global kx, ky, kz, nx, ny, nz    
#  print ('kx.shape=',kx.shape)


  nx = ny = nz = len(data['density'])
  if (nx > 16.1):
    nx, ny, nz = data.ds.domain_dimensions

  print ('n=',nx, ny, nz)

  L = (data.ds.domain_right_edge - data.ds.domain_left_edge).d

  kx = fftfreq(nx,d=L[0]*1.0/nx)
  ky = fftfreq(nx,d=L[1]*1.0/ny)
  kz = fftfreq(nx,d=L[2]*1.0/nz)

  print ('kx.shape=',kx.shape)  
  kx3d, ky3d, kz3d = meshgrid(kx, ky, kz, indexing="ij")
  k = np.sqrt(kx3d**2 + ky3d**2 + kz3d**2)
#  q0=data['density']
#  print ('q0.shape=', q0.shape)
#  print (len(data['density']))
  q1 = data['velocity_divergence']
#  print ('q1.shape=',q1.shape)
  q1_3d=reshape(q1,(nx,ny,nz))
#  q1_3d = q1
  q1_3d_k = fftn(q1_3d)
  phi_3d_k = q1_3d_k/k**2
  phi_3d_k[0][0][0] = 0.0
  phi_3d = ifftn(phi_3d_k)
  phi = phi_3d.ravel()
  phi_real = phi.real

  return phi_real


def see(i):
  global kx, ky, kz, nx, ny, nz    
  fn = get_fn(i)

  ds = yt.load(fn)
  ad = ds.all_data()

  c1 = [0.5,0.5,0.5]


#  q1 = ad['velocity_divergence']

  print (ad['number_density'])
  print (ad['phi_v'])
 
#  temp_grad_field = ds.add_gradient_fields(('gas','temperature'))
#  print (temp_grad_field)
#  bb = ad[temp_grad_field[0]]
#  print ('bb=',bb)

#  a1= (ad['density']).in_units('g/cm**3')
#  a1_3d=reshape(a1,(nx, ny, nz))
#  aa = a1_3d - rho*YTQuantity(1.0,'g/cm**3')
#  print ('aa=',aa)


def get_n_and_k(i):
   global kx, ky, kz, nx, ny, nz
   fn=get_fn(i)
   ds = yt.load(fn)
   dims1 = ds.domain_dimensions
   nx, ny, nz= dims1
   L = (ds.domain_right_edge - ds.domain_left_edge).d
 
   kx = fftfreq(nx,d=L[0]*1.0/nx)
   ky = fftfreq(nx,d=L[1]*1.0/ny)
   kz = fftfreq(nx,d=L[2]*1.0/nz)
      
#kx=ky=kz=0.
#nx=ny=nz=0.
#get_n_and_k(150)

#print ('kxxxxxx=',kx)

yt.add_field('number_density',function=_number_density, units  = '1/cm**3')
yt.add_field('phi_v',function=_phi_v)

num = [202,300,330]
num=range(600,601)
for i in num:
   see(i)

