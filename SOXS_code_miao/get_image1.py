#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import yt
#yt.enable_parallelism()
import pyxsim
import soxs
import aplpy

file_loc="data_for_aditi1/0826_HSE_1e-4_1e6K/DD0100/"
file_loc="DD0100/"
file_name = "sb_0100"
#file_name = "sb_0050"

#file_loc="data_for_aditi1/0810_uni_3e-5_3e6K/DD0050/"
ds = yt.load(file_loc + file_name)


slc = yt.SlicePlot(ds, "z", ["density", "temperature"], width=(0.8,"Mpc"))
slc.set_zlim("density",1.e-29,1.e-26)
slc.set_zlim("temperature",1.e4,1.e7)

slc.save()

sp = ds.sphere("c", (300.,"kpc"))

print(sp["density"].shape)

source_model = pyxsim.ThermalSourceModel("apec", 0.1, 2.0, 1000, nei=False ) #, model_vers="3.0.8")   # Zmet=1.0)

#thermal_model = pyxsim.ThermalSourceModel("apec", 0.1, 20.0, 10000, Zmet="metallicity")

exp_time = (2000., "ks") # exposure time
area = (3000.0, "cm**2") # collecting area
dist = (10, 'Mpc')
#redshift = 0.05


photons = pyxsim.PhotonList.from_data_source(sp, 0.0, area, exp_time, source_model, dist=dist)
photons.write_h5_file(file_name+"_photons.h5")

photons = pyxsim.PhotonList.from_file(file_name+"_photons.h5")

########## create event 

events = photons.project_photons("x", (45.,30.))
events.write_h5_file(file_name+ "_events.h5")
fov = (120.0, "arcmin") # the field of view / width of the image
nx = 120  # The resolution of the image on a side
events.write_fits_file(file_name + "_events.fits", fov, nx, overwrite=True)
events.write_simput_file(file_name+"_SOXS_events", overwrite=True, emin=0.1, emax=2.0)

######### create mock FITS image

#soxs.instrument_simulator(file_name+"_SOXS_events"+"_simput.fits", file_name+"evt_hdxi.fits", (100.0, "ks"),"hdxi", [45., 30.], overwrite=True)

#soxs.write_image(file_name+"evt_hdxi.fits",  file_name+"img_hdxi.fits", emin=0.1, emax=2.0, overwrite=True)

####### above Miao

#fig = aplpy.FITSFigure(file_name+"img_hdxi.fits")
#fig.show_colorscale(cmap='arbre', vmin=0.0, stretch='sqrt')
#fig.recenter(45., 30., radius=0.1)
#fig.add_colorbar()
#fig.save(file_name+"hdxi.png")


