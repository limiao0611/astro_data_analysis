#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy

file_loc="data_for_Pyxsim_CGM_180827_starafter2Gyr_6e-5SFR10_thenSFR1/DD0400/"
file_name = "sb_0400"

ds = yt.load(file_loc + file_name)


slc = yt.SlicePlot(ds, "z", ["density", "temperature"], width=(0.8,"Mpc"))
slc.set_zlim("density",1.e-29,1.e-26)
slc.set_zlim("temperature",1.e4,1.e7)

slc.save()

sp = ds.sphere("c", (200.,"kpc"))


emin=0.1
emax=2.0
nchan=1000
kT_min = 0.008
kT_max=10.
n_kT = 1000

#source_model = pyxsim.ThermalSourceModel("apec", emin=emin, emax=emax, nchan = nchan, kT_min = kT_min, kT_max=kT_max, n_kT = n_kT ,nei=False ) #, model_vers="3.0.8")   # Zmet=1.0)
source_model = pyxsim.ThermalSourceModel("apec", 0.1, 2.0, 1000, nei=False )

exp_time = (2000., "ks") # exposure time
area = (60000.0, "cm**2") # collecting area
dist = (5, 'Mpc')


photons = pyxsim.PhotonList.from_data_source(data_source=sp, redshift=0.0, area=area, exp_time=exp_time, source_model=source_model, dist=dist)
photons.write_h5_file(file_name+"_photons.h5")

#photons = pyxsim.PhotonList.from_file(file_name+"_photons.h5")

########## create event 

events = photons.project_photons("x", (45.,30.), absorb_model="wabs", nH=0.04)
events.write_h5_file(file_name+ "_events.h5")
fov = (70.0, "arcmin") # the field of view / width of the image
nx = 70  # The resolution of the image on a side
events.write_fits_file(file_name + "_events" + str(nx)+".fits", fov, nx, overwrite=True)
events.write_simput_file(file_name+"_events", overwrite=True, emin=0.1, emax=2.0)



