nohup xargs --arg-file=/home/ubuntu/feature_scripts/feature_tiles_redo.sh \
      --max-procs=1  \
      --replace \
      --verbose \
      /bin/sh -c "{}"
