# Miscellaneous

## Virtual Machines

The VMs can be managed on https://ui.hpccloud.surfsara.nl/.

## Server Scripts

The AHN3 data is downloaded and re-gridded to make the size of each tile small enough to work with. The re-gridded tiles are then normalised and the features are extracted.

### General Scripts

Once all VMs are up-and-running, the data storage can be mounted. All data live on a WebDAV server. Small amounts of data can temporarily be stored locally, but should eventually be copied onto the WebDAV server. To mount the WebDAV under _/data/_, run the _mount_all.sh_ script. Before the VMs is shut down, the _unmount_all.sh_ scripts can unmount this storage.

During the normalisation and feature extraction, _Server0_ will function as a masters, while the other VMs function as slaves. To allow _Server0_ to communicate with the other VMs, it must have _SSH_ access to them. The _copy_temp_key.sh_ script sends your local private key to the _/tmp/_ directory of _Server0_.

### Normalisation Scripts

Normalising a pointcloud means the height of the groundlevel is subtracted from the height of each point. Then, the _z_-coordinate of each point refers to the height-above-ground. This can be done using the _pdal_ library. Its documentation includes more information: https://pdal.io/stages/filters.hag.html.

The _normalise_copy_files.sh_ script first copies the other scripts onto the relevant VM. The _normalise_run_all.sh_ script can be started from within _Server0_ and starts up the procedure on all VMs. When you execute a Unix job in the background and logout from the session, your process will get killed. Our script avoids this using the _nohup_ method, so it is safe to log out of _Server0_.

On each VM, the _normalise_run_tiles_$f.sh_ script starts up the normalisation job. It includes the _pdal hag_ command to adjust the height-above-ground. As the list of all tiles is large, the _xargs_ method is used. This refers to a list of all tiles and iterates through the list, executing the same job for each of them. The _xargs_ methods allows the user to specify how many jobs each server sohuld do simultaneously. Taking care of the memory of each VM and the size of the input files, the normalisation script only run 2 jobs simultaneously. This list of tiles is located in the _normalise_tiles_$f.sh_ file.

The _normalise_get_lists.sh_ script can be run locally and downloads a list of all processed tiles from each server. This can be used in the _List Analysis Jupyter Notebook_ below to see what each VM has done so far.

Following the _List Analysis_, it may turn out some tiles where not processed. These should be investigated manually and, perhaps, retried. The _redo_ scripts allow this to be done easily.

Once all tiles have been processed, the output can be moved to the WebDAV server. The _normalise_move_all.sh_ script can be run from within _Server0_ and executes this move.

### Feature Scripts

Feature extraction...

## Jupyter Notebooks

Jupyter Notebooks...

### List Analysis

The _get_lists.sh_ scripts copy the list of processed tiles to the _Data_ directory discussed below. From there, the _ListAnalysis.ipynb_ reads the lists, together with the _tiles_list.txt_ files which contains the list of all tiles. It then compares the actual output with the expected output and shows how many tiles have already been processed and which ones still need to be processed.

### Data Conversion

Text.

### Data Verification

Text.

## Data

Text.

### Lists

Text.

### AHN3 Feature Data

Text.

### Terrain Data

Text.