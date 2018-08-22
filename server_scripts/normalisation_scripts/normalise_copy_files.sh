echo "Copying normalisation scripts to server 0"; \
scp normalise_run_all.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/normalisation_scripts/; \
scp normalise_move_all.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/normalisation_scripts/; \
scp normalise_run_tiles_redo.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/normalisation_scripts/; \
scp normalise_tiles_redo.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/normalisation_scripts/; \
scp normalise_move_redo.sh ubuntu@eecolidar0.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/normalisation_scripts/; \
for f in `seq 0 5`; do echo "Copying normalisation scripts to server $f"; scp normalise_run_tiles_$f.sh ubuntu@eecolidar$f.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/normalisation_scripts/; scp normalise_tiles_$f.sh ubuntu@eecolidar$f.eecolidar-nlesc.surf-hosted.nl:/home/ubuntu/normalisation_scripts/; done