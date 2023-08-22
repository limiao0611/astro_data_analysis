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

file_loc="data_for_aditi1/0826_HSE_1e-4_1e6K/DD0100/"
file_loc="DD0100/"
file_name = "sb_0100"
########

hubs= get_instrument_from_registry("mucal")
hubs['name']="hubs"
hubs['arf']= "hubs_cc_v20181102.arf" 
hubs['rmf']= "hubs_cc_v20181102.rmf"
hubs['bkgnd'] = None
hubs['fov']=60.
hubs['num_pixels']=3600
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
#instrument = 'mucal'
#instrument ='hdxi'
t_exp = 1000
exp_time = (t_exp, 'ks')
simput_file = file_name+"_SOXS_events_nx120_simput.fits"
#simput_file = file_name+"_SOXS_events"+"_simput.fits"
out_file = file_name+ "evt_convolved_"+instrument+'.fits'
sky_center = [45., 30.]

soxs.instrument_simulator (simput_file, out_file, exp_time, instrument, sky_center, overwrite=True)
emin = 0.1
emax= 2.0
out_image_file = file_name+"imgage_" + instrument+ ".fits"
soxs.write_image(out_file, out_image_file, emin = emin, emax=emax, overwrite=True)


####### above Miao

fig= aplpy.FITSFigure(out_image_file)
fig.show_colorscale(cmap='arbre', vmin=0.0, stretch='sqrt')
#fig.recenter(45., 30., radius=0.2)
fig.add_colorbar()
fig.save(file_name + instrument+ "convolved_texp" + str(t_exp)+ "ks.png")


