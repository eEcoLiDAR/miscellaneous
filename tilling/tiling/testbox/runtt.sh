#!/bin/bash

for s in $(seq 0 2)
do
    i=$s
    if [ $s -ne 2 ]
    then
	echo "running tt.sh on server $s"
	nohup ssh -i /Users/eslt0101/.ssh/id_rsa ubuntu@eecolidar$s.eecolidar-nlesc.surf-hosted.nl "/home/ubuntu/testbox/tt.sh $i >tf &"

    else
	echo "running tt.sh on man set 2"
	nohup ssh -i /Users/eslt0101/.ssh/id_rsa ubuntu@eecolidar$s.eecolidar-nlesc.surf-hosted.nl "/home/ubuntu/testbox/tt.sh 5 >tf &"
    fi
done
