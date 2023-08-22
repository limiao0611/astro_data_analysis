from numpy import *
from scipy.integrate import *
import matplotlib
import matplotlib.pyplot as plt

m_H = 1.67372e-24  # gram
kb = 1.38065e-16 #cgs
pi = 3.1415926535
pc = 3.0857e18 # cm
kpc=pc*1e3
year = 3.156e7 #s
Myr = year*1e6
mu = 0.6*m_H # mean molecular weight




def ReadCoolingCurve():
    FileIn = open("cool_rates.in_300K")
    data = loadtxt(FileIn)
    FileIn.close()
    return (data[:,0],data[:,1])

(LogT, LogCoolRate) = ReadCoolingCurve()

def LogCoolingRate(logT):
    return interp(logT, LogT, LogCoolRate)

def integrand(logT):
    return kb*10**logT * log(10.)/10**LogCoolingRate(logT)
#    return kb/(10**LogCoolingRate(logT))

def CoolingRate(T):
    return 10.0**interp(log10(T), LogT, LogCoolRate)

def CoolingRate_rev(T):
    return kb/CoolingRate(T)


def t_cool_ratio(T):
    t_integrate = quadrature(integrand, log10(T_min),log10(T),rtol=1e-5)[0]/year
    t_instantaneous =    kb* T/CoolingRate(T)/year
    return t_integrate/t_instantaneous 


T = 3e6
T_min=2e4
T_max=T
t_cool_instantaneous = kb* T/CoolingRate(T)/year
result= quadrature(CoolingRate_rev,T_min,T_max,rtol=1e-5)
#result1 = quad(integrand, log10(T_min),log10(T_max))
result1 = quadrature(integrand, log10(T_min),log10(T_max),rtol=1e-5)
#result1 = quadrature(integrand, T_min,T_max,rtol=1e-5)
t_cool_inte = result1[0]/year
print ('result: err/result=',result[0], result[1]/result[0])
print ('result1: err/result=',result1[0], result1[1]/result1[0])
print ('result/result1=',result[0]/result1[0])
print ('t_cool_instantaneous=%e'%t_cool_instantaneous)
print ('t_cool_inte=%e'%t_cool_inte)

print(CoolingRate(3e7)/CoolingRate(2e7))
print(log10(2e7))
print(log10(CoolingRate(2e7)))
print(log10(1e7))
print(log10(CoolingRate(1e7)))

T1 = 0.5e6*array(range(1,100))
t_ratio = []
for i in range(len(T1)):
    t_ratio.append(t_cool_ratio(T1[i]))

print ("T1=",T1)
print ("t_ratio=",t_ratio)

plt.semilogx(T1,t_ratio)

T2 = array([3e6,6e6,1e7,3e7])
t_ratio2 = []
for i in range(len(T2)):
    t_ratio2.append(t_cool_ratio(T2[i]))

plt.scatter(T2,t_ratio2,s=30)

plt.xlim(1e6,5e7)
plt.ylim(0.4,1.)

plt.xlabel("T [K]")
plt.ylabel("ratio: t_cool,2e4K / t_cool,0")
#plt.grid()
plt.savefig("cooling_time_ratio.pdf")
plt.show()
