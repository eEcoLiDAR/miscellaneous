xargs --arg-file=/home/ubuntu/normalisation_scripts/normalise_tiles_4.sh \
      --max-procs=2  \
      --replace \
      --verbose \
      /bin/sh -c "[ -f /data/local/eecolidar/rclone/tmp/ahn3_256x256_2km_norm/{}.LAZ ] && echo 'File {}.LAZ already exists' ||  echo 'Creating file {}.LAZ'; pdal translate /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_10_08_2018_256x256_2km/{}.LAZ /data/local/eecolidar/rclone/tmp/ahn3_256x256_2km_norm/{}.LAZ hag ferry --filters.ferry.dimensions='HeightAboveGround=Z';";