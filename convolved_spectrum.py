#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy
import astropy.io.fits as pyfits

from numpy import *
from soxs import get_instrument_from_registry, add_instrument_to_registry
soxs.show_instrument_registry()

########

hubs= get_instrument_from_registry("mucal")
hubs['name']="hubs"
hubs['arf']= "hubs_cc_v20181102.arf"
hubs['rmf']= "hubs_cc_v20181109.rmf"
hubs['bkgnd'] = None
hubs['fov']=60.
hubs['num_pixels']=60
hubs['aimpt_coords']= [0., 0.]
hubs['chips']= None
hubs['focal_length']= 10. # not sure
hubs['dither']= False
hubs['psf']= None
hubs['imaging']=True
hubs['grating']=False
name = add_instrument_to_registry(hubs)

######### create mock FITS image


file_loc="data_for_Pyxsim_CGM_180827_starafter2Gyr_6e-5SFR10_thenSFR1/DD0400/"
file_name = "sb_0400"



instrument ='hubs'
spec = soxs.Spectrum.from_file("all_spec.fits")
out_file = "convolved_spec.pha"
simulate_spectrum(spec, instrument, exp_time, out_file,
                  ptsrc_bkgnd=False, foreground=True,
                  instr_bkgnd=False, overwrite=True, nH=0.02,
                  absorb_model="tbabs", bkgnd_area=(1.0, "arcmin**2"))




f1 = pyfits.open("all_spec.pha")
fig = plt.figure(figsize=(9,7))
ax = fig.add_subplot(111)
ax.loglog(f1["SPECTRUM"].data["ENERGY"], f1["SPECTRUM"].data["COUNTS"])
ax.set_xlim(0.08, 2.3)
ax.set_xlabel("E (keV)")
ax.set_ylabel("counts/bin")
plt.savefig("all_spec_convolved.png")

