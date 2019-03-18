#!/bin/bash
source tiling.conf
source data_io.conf

inputTileList=$1
inputDir="$out_path_root"/"$aggregate_handle"
#inputDir="$out_path_root"/"test"
tempDir=$temp_path

xargs --arg-file="$inputTileList" \
      --max-procs=2 \
      -I{} \
      --verbose \
      /bin/bash -c "[ -f $inputDir/{}.LAZ ] && echo 'File {}.LAZ already present' || lasmerge -i  $inputDir/{}/*.LAZ -o $tempDir/{}.LAZ ; mv $tempDir/{}.LAZ $inputDir/{}.LAZ ;"


