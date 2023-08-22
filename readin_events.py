#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy

file_loc="data_for_Pyxsim_CGM_180827_starafter2Gyr_6e-5SFR10_thenSFR1/DD0400/"
file_name = "sb_0400"



#events=pyxsim.event_list.EventList.from_fits_file(file_name+ "_events.fits")
events=pyxsim.event_list.EventList.from_h5_file(file_name+ "_events.h5")
events.write_spectrum("all_spec.fits", 0.1, 2.0, 1000, overwrite=True)




