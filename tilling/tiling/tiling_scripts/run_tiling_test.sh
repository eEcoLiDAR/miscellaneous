#!/bin/bash

#expected arguments
# $1 : subset number


#-------------------

#read in data/output and tiling global parameters
#source data_io.conf
#source tiling.conf

echo `pwd`

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
echo "place holder mpc call for subset $1"
echo "input path is $inpath"
echo "output path is $outpath"
date 
#sleep 40 
echo "done sleeping"
date 
#mpc-tiling -i $inpath -o $outpath -t $temp_path -e $extent -n $number_of_cells -p $number_of_processes 1>$process_out_file 2>$process_err_file
