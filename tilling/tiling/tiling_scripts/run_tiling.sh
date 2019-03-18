#!/bin/bash

#expected arguments
# $1 : subset number


#-------------------

#read in data/output and tiling global parameters
. /home/ubuntu/tiling/data_io.conf
. /home/ubuntu/tiling/tiling.conf

#set variables
inpath="$in_path_root/$subset_handle$1/"
outpath="$out_path_root/$subset_handle$1/"
process_out_file="$handle_oe$1.out"
process_err_file="$handle_oe$1.err"

#create output directory if it doesn't exist
mkdir -p $outpath

#run tiling
echo "calling mpc-tiling"
mpc-tiling -i $inpath -o $outpath -t $temp_path -e "$extent" -n $number_of_cells -p $number_of_processes 1>$process_out_file 2>$process_err_file
