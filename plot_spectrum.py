import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy
from numpy import *

import astropy.io.fits as pyfits

f1 = pyfits.open("all_spec.fits")
#f2 = pyfits.open("line_spec.fits")
fig = plt.figure(figsize=(9,7))
ax = fig.add_subplot(111)

print(f1.info())
print(f1[1].columns)

print (len(f1["SPECTRUM"].data["ENERGY"]))
print ((f1["SPECTRUM"].data["COUNT_RATE"])/ f1["SPECTRUM"].data["COUNTS"])

ax.loglog(f1["SPECTRUM"].data["ENERGY"], f1["SPECTRUM"].data["COUNTS"])
#ax.loglog(f2["SPECTRUM"].data["ENERGY"], f2["SPECTRUM"].data["COUNTS"])

f1.close()
ax.set_xlim(0.08, 2.3)
#ax.set_ylim(1, 3.0e4)
ax.set_xlabel("E (keV)")
ax.set_ylabel("counts/bin")
plt.savefig("all_spec.png")
