#!/bin/bash


#---------------------------------------------------
#this script creates and sets up infrastructure as
#required for a tiling run
#
#
#---------------------------------------------------

#set up output directory
echo 'running output set up'
./setup_output_directory.sh


#copy ssh key top master
echo 'copying key'
./copy_key_to_master.sh

#create configuration file with full path to key on cluster
echo 'creating cluster key path' 
./create_cluster_key_path.sh
chmod 755 cluster_key_path.conf

#create tiling directory and copy relevant infrastructure to servers
echo 'setting up and copying infrastructure'
./copy_tiling_infra.sh



