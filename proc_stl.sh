#!/bin/bash


INPUT_PATH='/home/SUBTITULOS_TO_EDM/INPUT/'
OUTPUT_PATH='/home/SUBTITULOS_TO_EDM/OUTPUT/'
PROC_PATH='/home/SUBTITULOS_TO_EDM/INPUT/PROC/'

INPUT_PATH_OLD_TURNER='/home/SUBTITULOS_TO_EDM/INPUT_OLD_TURNER_FORMAT/'

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

for i in `ls -1 $INPUT_PATH_OLD_TURNER`
do
    if [ -f $INPUT_PATH_OLD_TURNER$i ]; then
	echo $i
	python /opt/packager/app/burn/adjusttc.py -i $INPUT_PATH_OLD_TURNER$i -o $OUTPUT_PATH$i -a '01:00:04;00' -n 2 
	if [ -f $OUTPUT_PATH$i ]; then
	    mv $INPUT_PATH_OLD_TURNER$i $PROC_PATH
	fi
    fi
done
