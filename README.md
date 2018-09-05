# Miscellaneous

This repository contains various scripts and files which are used in the eEcoLiDAR project. Most of these are used only once and, therefore, maintaining them does not have the highest priority.

## Virtual Machines

The VMs can be managed on https://ui.hpccloud.surfsara.nl/.

## Server Scripts

The AHN3 data is downloaded and re-gridded to make the size of each tile small enough to work with. The re-gridded tiles are then normalised and the features are extracted.

### General Scripts

Once all VMs are up-and-running, the data storage can be mounted. All data live on a WebDAV server. Small amounts of data can temporarily be stored locally, but should eventually be copied onto the WebDAV server. To mount the WebDAV under _/data/_, run the _mount_all.sh_ script. Before the VMs are shut down, the _unmount_all.sh_ scripts can unmount this storage.

During the normalisation and feature extraction, _Server0_ will function as a master, while the other VMs function as slaves. To allow _Server0_ to communicate with the other VMs, it must have _SSH_ access to them. The _copy_temp_key.sh_ script sends your local private key to the _/tmp/_ directory of _Server0_. This must be repeated every time the VM is shut down and rebooted.

### Normalisation Scripts

Normalising a pointcloud means the height of the groundlevel is subtracted from the height of each point. Then, the _z_-coordinate of each point refers to the height-above-ground. This can be done using the _pdal_ library. Its [documentation](https://pdal.io/stages/filters.hag.html) includes more information.

The _normalise_copy_files.sh_ script first copies the other scripts onto the relevant VM. Note that the VMs must already have the relevant directories, otherwise the copy will not succeed. The _normalise_run_all.sh_ script can be executed from within _Server0_ and starts up the normalisation procedure on all VMs. When you execute a Unix job in the background and logout from the session, your process will get killed. Our script avoids this using the _nohup_ method, so it is safe to log out of _Server0_ while the normalisation is running.

On each VM, the _normalise_run_tiles_x.sh_ script starts up the normalisation job. It includes the _pdal hag_ command to adjust the height-above-ground. As the list of all tiles is large, the _xargs_ method is used. This refers to a list of all tiles and iterates through the list, executing the same job for each of them. The _xargs_ methods allows the user to specify how many jobs each server should do simultaneously. Taking care of the memory of each VM and the size of the input files, the normalisation script only runs 2 jobs simultaneously. This list of tiles is located in the _normalise_tiles_x.sh_ file.

The _normalise_get_lists.sh_ script can be run locally and downloads a list of all processed tiles from each server. This can be used in the _List Analysis_ _Jupyter Notebook_, discussed below, to see what each VM has done so far.

Following the _List Analysis_, it may turn out some tiles where not processed. These should be investigated manually and, perhaps, re-done. The _redo_ scripts allow this to be executed easily.

Once all tiles have been processed, the output can be moved from the VMs to the WebDAV server. The _normalise_move_all.sh_ script can be run from within _Server0_ and executes this move.

### Feature Scripts

The feature extraction scripts follow a similar logic to the normalisation scripts. In particular, the _feature_copy_files.sh_ script copies the other scripts to the relevant VM. The _feature_run_all.sh_ script can be used from _Server0_ to start the feature extraction. The _feature_run_tiles_x.sh_ scripts include the command which executes the feature extraction. This uses the _computefea_wtargets_cell.py_ Python script to call the _LaserChicken_ module, which calculates the features. The _feature_tiles_x.sh_ files contain the list of tiles per VM. The _feature_move_all.sh_ script moves the output _.ply_ files to the WebDAV server. There are also redo scripts, similar to the normalisation procedure. The _feature_get_lists.sh_ script downloads the list of tiles which have already been processed. Finally, the _feature_get_files.sh_ downloads the output files to the local environment, such that they can be further processed by the _Data Conversion_ _Jupyter Notebook_.

## Jupyter Notebooks

There are three _Jupyter Notebooks_ which help analyse and convert the data.

### List Analysis

The _get_lists.sh_ scripts copy the lists of processed tiles to the _data_ directory discussed below. From there, the _ListAnalysis.ipynb_ reads the lists, together with the _tiles_list.txt_ file which contains the list of all tiles. It then compares the actual output with the expected output and shows how many tiles have already been processed and which ones still need to be processed.

### Data Conversion

The output of LaserChicken are _.ply_ files, one for each input tile. These files contain a number of points, depending on the chosen resolution, which have the features as attributes. The _DataConversion.ipynb_ reads these _.ply_ files using the _plyfile_ module. It joins the files into one dataset and converts this to a _compressed Numpy array_ and to a _GeoTiff_.

### Data Verification

To verify that the features are correctly extracted, the _DataVerification.ipynb_ reads the _.npz_ version of the data and prints various details for each feature. This is, then, compared with the expected details for each feature.

## Data

The _data_ directory of this repository contains various output files related to the normalisation and feature extraction procedures.

### Lists

This directory contains the _tiles_list.txt_ files which is a list of all tiles. It also contains all lists downloaded by the _get_lists.sh_ scripts of the normalisation and feature extraction.

### AHN3 Feature Data

The _feature_get_lists.sh_ script downloads all _.ply_ files from the various VMs and places them in the _data_ directory, in a separate directory per resolution.

### Terrain Data

The _Data Conversion_ _Jupyter Notebook_ places the _compressed Numpy array_ and the _GeoTiff_ with the terrain features in the _data_ directory.