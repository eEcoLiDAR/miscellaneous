for f in `seq 0 5`; do echo "Mounting WebDAV to server $f"; ssh ubuntu@eecolidar$f.eecolidar-nlesc.surf-hosted.nl "/home/ubuntu/mount_dl.sh"; done;
