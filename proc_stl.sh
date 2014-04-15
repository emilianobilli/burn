#!/bin/bash


INPUT_PATH='/home/SUBTITULOS_TO_EDM/INPUT/'
OUTPUT_PATH='/home/SUBTITULOS_TO_EDM/OUTPUT/'
PROC_PATH='/home/SUBTITULOS_TO_EDM/INPUT/PROC/'


for i in `ls -1 $INPUT_PATH`
do
    if [ -f $INPUT_PATH$i ]; then
	echo $i
	python /opt/packager/app/burn/adjusttc.py -i $INPUT_PATH$i -o $OUTPUT_PATH$i -a '01:00:04;00' -n 1 -f -p '8X'
	if [ -f $OUTPUT_PATH$i ]; then
	    mv $INPUT_PATH$i $PROC_PATH
	fi
    fi
done
