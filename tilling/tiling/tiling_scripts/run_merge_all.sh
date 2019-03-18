#!/bin/bash

source data_io.conf
source tiling.conf
source cluster_info.conf
source cluster_key_path.conf

retiledSetListHandle="$out_path_root"/"$retiled_handle"

vm_max=$(($number_vms -1))

for i in $(seq 0 $vm_max)
do

    retiledSetList="$retiledSetListHandle""$i".txt

    if [ $i -ne $master_server_number ]
    then
	echo "running merging on server $i"
	#nohup ssh -i $full_key_path $user@$server_name_root$i.$server_extension "$tiling_path/run_merge.sh $retiledSetList &"
        ssh -i $full_key_path $user@$server_name_root$i.$server_extension "/bin/bash -c \"((nohup $tiling_path/run_merge.sh $retiledSetList > merge.out 2>1) &)\""

    else
	echo "running merging on master server $master_server_number"
	#nohup $tiling_path/run_merge.sh $retiledSetList &
        /bin/bash -c "((nohup $tiling_path/run_merge.sh $retiledSetList > merge.out 2>1) &)"

    fi
    
done
