import yt
import matplotlib
import matplotlib.pyplot as plt
from yt.units import second, gram, parsec,centimeter, erg
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

def _cell_etot(field, data):
    return data['cell_mass']*data['TotalEnergy']

def _cell_eth(field, data):
    return data['cell_mass']*data['GasEnergy']


def _cell_ek(field, data):
    return data['cell_etot'] - data['cell_eth']

def _cell_cool_rate(field, data):
    return data['cell_eth']/data['cooling_time']

def _cell_metal_mass(field, data):
    return data['metal_density']*data['cell_volume']

yt.add_field('cell_etot',function = _cell_etot, units='erg')
yt.add_field('cell_eth',function = _cell_eth, units='erg')
yt.add_field('cell_ek',function = _cell_ek, units='erg')
yt.add_field('cell_cool_rate',function=_cell_cool_rate, units='erg/yr')
yt.add_field('cell_metal_mass', function=_cell_metal_mass, units='Msun')



num=range(10,200,10)
num=range(0,850,50)

for i  in num:
    filen = get_fn(i)
    print (filen)
    ds = yt.load(filen)
    ad = ds.all_data()
    t = ds.current_time.in_units('Myr')

    mZ_tot = ad['cell_metal_mass'].sum().in_units('msun')    
    cool = ad.cut_region("obj['temperature'].in_units('K')<3e4")
    hot = ad-cool
    mZ_c = cool['cell_metal_mass'].sum().in_units('msun') 

    m_c = cool['cell_mass'].sum().in_units('msun')
    m_h = hot['cell_mass'].sum().in_units('msun')
 
    ism = ad.cut_region(" (obj['z'].in_units('kpc')<3) & (obj['z'].in_units('kpc')>-3) & (obj['radius'].in_units('kpc')<10)  " )
    cgm = ad-ism

    cgm_h = cgm.cut_region("obj['temperature'].in_units('K')>3e4")
    mZ_ism = ism['cell_metal_mass'].sum().in_units('msun')    
    mZ_cgm = cgm['cell_metal_mass'].sum().in_units('msun')    
    mZ_cgm_h = cgm_h['cell_metal_mass'].sum().in_units('msun')    

    V_ism = ism['cell_volume'].sum().in_units('kpc**3')
    V_cgm=cgm['cell_volume'].sum().in_units('kpc**3')
    V = ad['cell_volume'].sum().in_units('kpc**3')
    f3=open('mZ_t.dat','a') 
#    print (t, mZ_tot, mZ_ism, V_ism)
    print  (t, mZ_tot, mZ_ism, mZ_cgm, mZ_cgm_h ,mZ_c, m_c, m_h, file=f3)
    f3.close()

    
