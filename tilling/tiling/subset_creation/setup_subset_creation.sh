#this scripts creates and populatews infrastructure on
#the cluster master server to run tile subset creation
#It makes use of the configuration files located in the
#setup_scripts directory of the tiling run

source ../setup_scripts/local_sys_info.conf
source ../setup_scripts/cluster_info.conf
#source ../setup_scripts/data_io.conf

ssh -i $local_key_path/$key_file $user@$server_name_root$master_server_number.$server_extension "mkdir -p $tiling_path/subset_creation"


scp subset_info.conf $user@$server_name_root$master_server_number.$server_extension:$tiling_path/subset_creation/
scp create_subset_lists.sh $user@$server_name_root$master_server_number.$server_extension:$tiling_path/subset_creation/
scp create_subset_and_populate_subset_folders.sh $user@$server_name_root$master_server_number.$server_extension:$tiling_path/subset_creation/
scp create_subsets.sh $user@$server_name_root$master_server_number.$server_extension:$tiling_path/subset_creation/
