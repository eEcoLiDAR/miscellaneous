#!/bin/bash

#read in data/output and tiling global parameters
. /home/ubuntu/tiling/data_io.conf
. /home/ubuntu/tiling/tiling.conf
. /home/ubuntu/tiling/cluster_info.conf


current_directory=`pwd`

allTilesDir="$out_path_root"/"$aggregate_handle"
allTilesList="$out_path_root"/"$aggregate_handle"_list.txt
retiledSubList="$out_path_root"/"$retiled_handle"

#cd $allTilesDir

ntiles=$(ls  $allTilesDir | wc -l)
echo $ntiles


ls $allTilesDir > $allTilesList

#size of set
echo $number_vms
size_set=$(($ntiles/$number_vms))
echo $size_set

#remainder setsize
remainder_set=$(($ntiles%$number_vms))
echo $remainder_set

#define top set index
max_set=$(($number_vms - 1))

echo $max_set

for i in $(seq 0 $max_set)
do
if [ $i -eq $max_set ]
then
    set_first_line=$((1+(i*size_set)))
    set_last_line=$(((i+1)*size_set + remainder_set))
    echo $set_first_line
    echo $set_last_line
    sed -n "$set_first_line,$set_last_line p" $allTilesList > "$retiledSubList""$i".txt
else
    set_first_line=$((1+(i*size_set)))
    set_last_line=$(((i+1)*size_set))
    echo $set_first_line
    echo $set_last_line
    sed -n "$set_first_line,$set_last_line p" $allTilesList > "$retiledSubList""$i".txt
fi
    
done
#change directory back to original
#cd $current_directory
