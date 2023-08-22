from numpy import *
import matplotlib
import  matplotlib.pyplot as plt

f=open("cool_rates.in_300K")
T, cool1, cool2 = loadtxt(f, usecols=(0,1,2),unpack = True )
plt.plot(T, cool1)
plt.plot(T, cool2)
plt.grid()
#plt.ylim(-24,-21)
plt.show()
