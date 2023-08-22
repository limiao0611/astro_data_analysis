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

num=[0,1,2,5,10,50,100,200,300,400,500]
for i  in num:
    filen = get_fn(i)
    print (filen)
    ds = yt.load(filen)
    c1=[0., 0., 0.]
    sphere = ds.sphere( center=c1,radius = (200,'kpc'))
#    sphere = ds.all_data()
#    ad = ds.all_data()
    t=ds.current_time.in_units("Myr")
    m = sphere.quantities.total_quantity (['cell_mass']).in_units("Msun")   
    etot = sphere.quantities.total_quantity (['cell_etot'])   
    eth = sphere.quantities.total_quantity (['cell_eth'])   
    ek = sphere.quantities.total_quantity (['cell_ek'])  
    cool_rate = sphere.quantities.total_quantity(['cell_cool_rate']) 
    m_met = sphere.quantities.total_quantity(['cell_metal_mass'])  
 
    print ("t, m, m_met,  etot, eth, ek, cool_rate =%f,  %e,  %e, %e %e, %e, %e"%(t,m, m_met, etot, eth, ek, cool_rate))
 
    f3=open("e_m_t.dat",'a')
    print ("t, m, m_met, etot, eth, ek, cool_rate(erg/yr) =%f,  %e,  %e, %e, %e,  %e, %e"%(t,m, m_met,  etot, eth, ek, cool_rate), file = f3)
    f3.close()

    
