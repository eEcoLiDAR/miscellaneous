#!/bin/bash

#this assumes the data storage is mounted already

source local_sys_info.conf
source data_io.conf
source cluster_info.conf


#create output root directory
echo 'creating output path root directory'
ssh -i $local_key_path/$key_file $user@$server_name_root$master_server_number.$server_extension "mkdir -p $out_path_root ;"

