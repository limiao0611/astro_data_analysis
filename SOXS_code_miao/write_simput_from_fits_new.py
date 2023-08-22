#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy

file_loc="DD0100/"
file_name = "sb_0100"



fov=(120,'arcmin')
nx=120
events=pyxsim.event_list.EventList.from_fits_file(file_name+ "_events.fits")


events.write_simput_file(file_name+"_SOXS_events_nx"+str(nx), overwrite=True, emin=0.1, emax=2.0)



