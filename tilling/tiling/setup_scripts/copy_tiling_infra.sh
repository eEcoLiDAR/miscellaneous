#!/bin/bash

source cluster_info.conf
source local_sys_info.conf

vm_max=$(($number_vms -1))

for s in $(seq 0 $vm_max)
do

    echo "setting up server $s"
    ssh -i $local_key_path/$key_file $user@$server_name_root$s.$server_extension "mkdir -p $tiling_path"
    scp ../tiling_scripts/run_tiling.sh $user@$server_name_root$s.$server_extension:$tiling_path/
    scp ../tiling_scripts/run_tiling_test.sh $user@$server_name_root$s.$server_extension:$tiling_path/
    scp ../tiling_scripts/run_validation.sh $user@$server_name_root$s.$server_extension:$tiling_path/
    scp ../tiling_scripts/run_validation_test.sh $user@$server_name_root$s.$server_extension:$tiling_path/
    scp ../tiling_scripts/tiling.conf $user@$server_name_root$s.$server_extension:$tiling_path/
    scp data_io.conf $user@$server_name_root$s.$server_extension:$tiling_path/

    scp ../tiling_scripts/run_merge.sh $user@$server_name_root$s.$server_extension:$tiling_path/

    if [ $s -eq $master_server_number ]
    then
 	scp ../tiling_scripts/run_tiling_all.sh $user@$server_name_root$s.$server_extension:$tiling_path/
	scp ../tiling_scripts/run_tiling_all_test.sh $user@$server_name_root$s.$server_extension:$tiling_path/
        scp ../tiling_scripts/run_validation_all.sh $user@$server_name_root$s.$server_extension:$tiling_path/
	scp ../tiling_scripts/run_validation_all_test.sh $user@$server_name_root$s.$server_extension:$tiling_path/

        scp ../tiling_scripts/aggregate_tiles.sh $user@$server_name_root$s.$server_extension:$tiling_path/
	scp ../tiling_scripts/collect_tiles.py $user@$server_name_root$s.$server_extension:$tiling_path/
	scp ../tiling_scripts/move_tiles.py $user@$server_name_root$s.$server_extension:$tiling_path/

	scp ../tiling_scripts/create_retiled_sets.sh $user@$server_name_root$s.$server_extension:$tiling_path/

	scp ../tiling_scripts/run_merge_all.sh $user@$server_name_root$s.$server_extension:$tiling_path/
	
	scp cluster_info.conf $user@$server_name_root$s.$server_extension:$tiling_path/
	scp cluster_key_path.conf $user@$server_name_root$s.$server_extension:$tiling_path/
    fi
    
    
done
