# AHN2_waterpipe
Python / PDAL pipeline to classify water returns in the AHN2 point cloud data set using a data imminent method.

## Current Status
The pipelines and scripts in this repository are currently still in the initial testing/validation phase.
The processing pipeline is designed to be run remotely in a distributed fashion for the entire data set. Beware,
run time for a ca. 1km x1km subtile is approx. 4.5 min.

### Pre-requisites
The PDAL library needs to be installed as well as Python 3+ including mumpy and invoke packages. 
