#!/bin/bash

#expected arguments
# $1 data directory
# $2 number of subsets
# $2 subset_file_handle

#---------

#change directory to data directory
current_directory=`pwd`
cd $1


#define top set index
max_set=$(($2-1))

echo $max_set

for i in $(seq 0 $max_set)
do
mkdir -p $3_$i

#replace xargs with gxargs if running on mac with gnu xargs installed, e.g via homebrew. xargs will cause errors
xargs --arg-file=$3_$i.txt \
      --max-args=1 \
      --max-procs=4 \
      --replace \
      mv {} ./$3_$i/  ;

done
    
#change directory back to original
cd $current_directory
