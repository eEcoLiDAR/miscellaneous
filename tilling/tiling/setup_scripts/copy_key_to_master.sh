#!/bin/bash

source local_sys_info.conf
source cluster_info.conf

scp $local_key_path/$key_file $user@$server_name_root$master_server_number.$server_extension:$key_path/



