#!/bin/bash

#this file is located in the setup_scripts subdirectory in the repository and is copied into the tiling_scripts directory on the VMs
source cluster_info.conf
source cluster_key_path.conf

vm_max=$(($number_vms -1))

for s in $(seq 0 $vm_max)
do
    if [ $s -ne $master_server_number ]
    then
	echo "running validation on server $s"
	#nohup ssh -i $full_key_path $user@$server_name_root$s.$server_extension "$tiling_path/run_validation.sh $s &" 
        ssh -i $full_key_path $user@$server_name_root$s.$server_extension "/bin/bash -c \"((nohup $tiling_path/run_validation.sh $s > validation.pot 2>1) &)\""

    else
	echo "running validation on master server $master_server_number"
	#nohup $tiling_path/run_validation.sh $s &
        /bin/bash -c "((nohup $tiling_path/run_validation.sh $s > validation.out 2>1) &)"

    fi
done
