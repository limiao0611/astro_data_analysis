#This program takes the raw data from simulations 
#and produces images for a particular instrument.


import yt
#yt.enable_parallelism()
import pyxsim
import soxs
#import aplpy

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

sp = ds.sphere("c", (500.,"kpc"))

print(sp["density"].shape)

source_model = pyxsim.ThermalSourceModel("apec", 0.005, 11.0, 10000, Zmet=1.0)

exp_time = (500., "ks") # exposure time
area = (2000.0, "cm**2") # collecting area
#redshift = 0.05


photons = pyxsim.PhotonList.from_data_source(sp, 0.0, area, exp_time, source_model, dist=(10.0,'Mpc'))
photons.write_h5_file(file_name+"_photons.h5")

events_z = photons.project_photons("z", (45.,90.))

soxs.instrument_simulator("hse_simput.fits", file_loc+"evt.fits", (100.0, "ks"),"hdxi", [45., 30.], overwrite=True)

soxs.write_image(file_loc+ "evt.fits", file_loc + "img.fits", emin=0.001, emax=1.0, overwrite=True)

fig = aplpy.FITSFigure(file_loc+"img.fits")
fig.show_colorscale(cmap='arbre', vmin=0.0, stretch='sqrt')
fig.recenter(45., 30., radius=0.1)
fig.add_colorbar()
fig.save(file_loc+"z0.05.png")


