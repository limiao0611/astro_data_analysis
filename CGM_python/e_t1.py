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

num = range(56,60)
num=[300,301]
num=[298,299]
num=range(10,200,10)

for i  in num:
    filen = get_fn(i)
    print (filen)
    ds = yt.load(filen)
    ad = ds.all_data()
    specific_energy_unit = ds.length_unit**2/ds.time_unit**2
    a = ds.current_time
    b= ds.time_unit
    time = a*b/second/3.15e7 
    total1 = sum(ad["enzo","TotalEnergy"]*ad['cell_mass']*specific_energy_unit).in_units('erg')
    thermal1 = sum(ad["enzo","GasEnergy"]*ad['cell_mass']).in_units('erg')
    T_min = min(ad["enzo","Temperature"])
    T_max = max(ad["enzo","Temperature"])
    f3=open("e_t1.dat",'a')
#    print>>f3, (time,total1,thermal1)
    print (time,total1,thermal1,T_min,T_max)
    print  (time,total1,thermal1,T_min,T_max, file=f3)
    f3.close()

    
