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

file_loc="data_for_aditi1/0826_HSE_1e-4_1e6K/DD0100/"
file_loc="DD0100/"
file_name = "sb_0100"
t_exp = 1000
instrument='hubs'
out_image_file = file_name+"_events120.fits"

####### above Miao

#event = pyxsim.event_list.EventList.from_fits_file(file_name+"_events120.fits" )
#event.write_fits_image(file_name + "events_output.fits" , emin=0.1, emax=2.0, nx=120, fov=(120,'arcmin'))

fig= aplpy.FITSFigure(file_name + "events_output.fits")
fig.show_colorscale(cmap='arbre', vmin=0.0, stretch='sqrt') #,  smooth=33)
#fig.recenter(45., 30., radius=0.3)
fig.add_colorbar()
fig.save(file_name + "events_output.png")


