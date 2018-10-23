# Generate Feature Scripts
Automatically generate the server scripts required for running Laserchicken on the surfsara hosted cluster of VMs.

The structure of the server scripts is largely generic to an implementation of a remotely hosted cluster of virtual machines.
Accordingly, the generation of server scripts aims to take arguments allowing the user to adapt the scripts to their own
purposes, even if the actual cluster is not hosted by surfsara. Nevertheless, the use case for which the scripts are provided
is the calculation of features in cells (of a specified size) using laserchicken on a cluster of VMs hosted by surfsara.

## Requirements
Python 3+

numpy

## Input
All input arguments to the `generate_feature_script_cell.py` script are provided in the input file which is passed to script.

The required directory structure must be in place before the produced scripts are run.

The actual feature extraction script which contains the call to and instructions for laserchicken must be provided separately.

By retaining the input file and the feature extraction script the specifics of each run can efficiently be retained in a
reproducible fashion

## Running
The `generate_feature_script_cell.py` should be run in the directory which contains its `input file`. This can be done as
`python generate_feature_script_cell.py inputfile.txt`.

An intial example of an input file is provided as `ahn3_100m_filtered_scriptgen_input.txt`.

