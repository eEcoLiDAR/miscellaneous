nohup xargs --arg-file=/home/ubuntu/normalisation_scripts/normalise_tiles_redo.sh \
      --max-procs=1  \
      --replace \
      --verbose \
      /bin/sh -c "{}"
