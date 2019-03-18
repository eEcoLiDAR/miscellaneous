#!/bin/bash

#this file is located in the setup_scripts subdirectory in the repository and is copied into the tiling_scripts directory on the VMs
source cluster_info.conf
source cluster_key_path.conf


vm_max=$(($number_vms -1))

for s in $(seq 0 $vm_max)
do
    if [ $s -ne $master_server_number ] ; then
	echo "running tiling on server $s"
	#echo "palce holder command execution"
	nohup ssh -i $full_key_path $user@$server_name_root$s.$server_extension "$tiling_path/run_tiling_test.sh $s; " & 

    else
	echo "running tiling on master server $master_server_number"
	#echo "master palce holder command execution"
	nohup $tiling_path/run_tiling_test.sh $s &
    fi
done

