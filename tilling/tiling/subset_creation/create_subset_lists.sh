#!/bin/bash

#expected arguments:
# $1 : data directory
# $2 : number of sets to create
# $3 : subset file handle

#------------------------------------

#change directory to data directory

current_directory=`pwd`
cd $1

#number of relevant files
nf=$(ls -l *.LAZ | wc -l)


#create list of all files
echo 'getting file list'
ls *.LAZ > all_tiles_list.txt 


#create (equal size) subsets of files. initially create lists denoting each subset

#size of set
size_set=$(($nf/$2))
echo $size_set

#remainder setsize
remainder_set=$(($nf%$2))
echo $remainder_set

#define top set index
max_set=$(($2-1))
#if [max_set==0]
#   echo 'no creation of sets required. exiting'
#   exit
#fi

echo $max_set

for i in $(seq 0 $max_set)
do
if [ $i -eq $max_set ]
then
    set_first_line=$((1+(i*size_set)))
    set_last_line=$(((i+1)*size_set + remainder_set))
    echo $set_first_line
    echo $set_last_line
    sed -n "$set_first_line,$set_last_line p" all_tiles_list.txt > $3_$i.txt
else
    set_first_line=$((1+(i*size_set)))
    set_last_line=$(((i+1)*size_set))
    echo $set_first_line
    echo $set_last_line
    sed -n "$set_first_line, $set_last_line p" all_tiles_list.txt > $3_$i.txt
fi
    
done

#change directory back to original
cd $current_directory




