echo "Copying feature scripts to server 0"; \
scp feature_run_all.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; \
scp feature_move_all.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; \
scp feature_run_tiles_redo.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; \
scp feature_tiles_redo.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; \
scp feature_move_redo.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; \
for f in `seq 0 5`; do echo "Copying feature scripts to server $f"; echo $f; scp computefea_wtargets_cell.py ubuntu@eecolidar$f.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; scp feature_run_tiles_$f.sh ubuntu@eecolidar$f.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; scp feature_tiles_$f.sh ubuntu@eecolidar$f.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/feature_scripts/; done