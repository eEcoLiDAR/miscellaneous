for f in `seq 1 5`; do nohup ssh -i /tmp/id_rsa ubuntu@eecolidar$f.eecolidar-nlesc.surf-hosted.nl "/bin/cp -rf /data/local/eecolidar/rclone/tmp/ahn3_256x256_2km_norm/ /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/" & done; \
nohup /bin/cp -rf /data/local/eecolidar/rclone/tmp/ahn3_256x256_2km_norm/ /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/