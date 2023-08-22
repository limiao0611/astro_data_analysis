#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import matplotlib
matplotlib.use('Agg')
import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy
from numpy import *
from soxs import get_instrument_from_registry, add_instrument_to_registry
soxs.show_instrument_registry()


file_loc="data_for_Pyxsim_CGM_180827_starafter2Gyr_6e-5SFR10_thenSFR1/DD0400/"
file_name = "sb_0400"

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
instrument = 'hubs'
#instrument = 'athena_wfi'
#instrument = 'mucal'
#instrument ='hdxi'
t_exp = 2000
exp_time = (t_exp, 'ks')
simput_file = file_name+"_events"+"_simput.fits"
out_file = file_name+ "convolved_"+instrument+'.fits'
sky_center = [45., 30.]

soxs.instrument_simulator (simput_file, out_file, exp_time, instrument, sky_center, overwrite=True, ptsrc_bkgnd=True,
                          instr_bkgnd=False, foreground=True)
emin = 0.1
emax= 2.0
out_image_file = file_name+"convolved_imgage_" + instrument+ ".fits"

soxs.write_image(out_file, out_image_file, emin = emin, emax=emax, overwrite=True)



fig= aplpy.FITSFigure(out_image_file)
fig.show_colorscale(cmap='arbre', vmin=0.0 , vmax= 7e4) #, stretch='sqrt')
fig.recenter(45., 30., radius=0.55)
fig.add_colorbar()
fig.save(file_name + instrument+ "_texp" + str(t_exp)+ "ks_60pixel_1109rmf_nobackground.png")


