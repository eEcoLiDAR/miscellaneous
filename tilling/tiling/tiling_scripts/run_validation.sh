#!/bin/bash

#expected arguments
#$1 : subset number

#read in data/output and tiling global parameters
. /home/ubuntu/tiling/data_io.conf
. /home/ubuntu/tiling/tiling.conf


inpath="$in_path_root/$subset_handle$1/"
outpath="$out_path_root/$subset_handle$1/"
dbpath="$database_path/"
dbname="$dbname_handle"_"$1"

echo "running validation for $subset_handle$1 "
mpc-validate-tiles -l $dbpath -n $dbname -i $inpath -t $outpath 
