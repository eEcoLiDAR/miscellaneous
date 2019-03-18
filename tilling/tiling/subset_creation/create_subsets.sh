#!/bin/bash

source subset_info.conf


#---------

echo "creating $number_subsets subsets from files in directory $data_path"

echo "creating subset lists"
./create_subset_lists.sh $data_path $number_subsets $subset_handle

echo 'creating and populating subset folders'
./create_subset_and_populate_subset_folders.sh $data_path $number_subsets $subset_handle


