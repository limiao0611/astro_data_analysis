#!/bin/bash
#SBATCH -N1 --ntasks-per-node=27 --exclusive -o OUTPUT  -p bnlx
#SBATCH --mail-user=mli@flatironinstitute.org
#SBATCH --mail-type=ALL
#SBATCH -t 00-02:30:00
#source ~/.bash_profile
module load nix
module load nix/gcc nix/hdf5-openmpi1 # or -openmpi2
#module load gcc openmpi
#export LD_LIBRARY_PATH=$YT_DEST/lib:$LD_LIBRARY_PATH
#python get_image1.py >>output_get_image1 
#python make*.py >>output_make_mock_image 
#python make*hubs.py >>output_make_mock_image 
#python write_simput*fits.py 
python create*py
python make_convolved*py
#python make_event_fits_image_new.py
python readin_events.py

