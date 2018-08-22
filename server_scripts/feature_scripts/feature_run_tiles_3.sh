xargs --arg-file=/home/ubuntu/feature_scripts/feature_tiles_3.sh \
      --max-procs=3  \
      --replace \
      --verbose \
      /bin/sh -c "[ -f /data/local/eecolidar/rclone/tmp/ahn3_feature_10m/{}.ply ] && echo 'File {}.ply already exists' ||  echo 'Creating file {}.ply'; python /home/ubuntu/feature_scripts/computefea_wtargets_cell.py /data/local/eecolidar/modules/python/laserchicken/ /data/local/eecolidar/rclone/tmp/ahn3_256x256_2km_norm/{}.LAZ /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_targets_10m/{}_target.laz 5 /data/local/eecolidar/rclone/tmp/ahn3_feature_10m/{}.ply;"