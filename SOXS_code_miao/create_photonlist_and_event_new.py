#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy

file_loc="DD0100/"
file_name = "sb_0100"

ds = yt.load(file_loc + file_name)


slc = yt.SlicePlot(ds, "z", ["density", "temperature"], width=(0.8,"Mpc"))
slc.set_zlim("density",1.e-29,1.e-26)
slc.set_zlim("temperature",1.e4,1.e7)

slc.save()

sp = ds.sphere("c", (300.,"kpc"))




exp_time = (2000., "ks") # exposure time
area = (3000.0, "cm**2") # collecting area
dist = (10, 'Mpc')


source_model = pyxsim.ThermalSourceModel("apec", 0.1, 2.0, 1000, nei=False ) #, model_vers="3.0.8")   # Zmet=1.0)
photons = pyxsim.PhotonList.from_data_source(data_source=sp, redshift=0.0, area=area, exp_time=exp_time, source_model, dist=dist)
photons.write_h5_file(file_name+"_photons.h5")

photons = pyxsim.PhotonList.from_file(file_name+"_photons.h5")

########## create event 

events = photons.project_photons("x", (45.,30.))
events.write_h5_file(file_name+ "_events.h5")
fov = (120.0, "arcmin") # the field of view / width of the image
nx = 120  # The resolution of the image on a side
events.write_fits_file(file_name + "_events" + str(nx)+".fits", fov, nx, overwrite=True)
events.write_simput_file(file_name+"_events", overwrite=True, emin=0.1, emax=2.0)



