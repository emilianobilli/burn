#!/bin/bash


INPUT_VENUS_PATH='/home/SUBTITULOS_TO_EDM/INPUT_VENUS/'
INPUT_PLAYBOY_PATH='/home/SUBTITULOS_TO_EDM/INPUT_PLAYBOY/'
OUTPUT_PATH='/home/SUBTITULOS_TO_EDM/OUTPUT/'
PROC_PATH='/home/SUBTITULOS_TO_EDM/PROC/'

INPUT_PATH_OLD_TURNER='/home/SUBTITULOS_TO_EDM/INPUT_OLD_TURNER_FORMAT/'
TURNER_PROC_PATH='/home/SUBTITULOS_TO_EDM/INPUT_OLD_TURNER_FORMAT/PROC/'

for i in `ls -1 $INPUT_VENUS_PATH`
do
    if [ -f $INPUT_VENUS_PATH$i ]; then
	echo $i
	python /opt/packager/app/python-stl-ebu/adjusttc.py -i $INPUT_VENUS_PATH$i -o $OUTPUT_PATH$i -a '00:00:05;00' -n 1 -f -p '8X'
	if [ -f $OUTPUT_PATH$i ]; then
	    mv $INPUT_VENUS_PATH$i $PROC_PATH
	fi
    fi
done

for i in `ls -1 $INPUT_PLAYBOY_PATH`
do
    if [ -f $INPUT_PLAYBOY_PATH$i ]; then
	echo $i
	python /opt/packager/app/python-stl-ebu/adjusttc.py -i $INPUT_PLAYBOY_PATH$i -o $OUTPUT_PATH$i -a '00:00:04;00' -n 1 -f -p '8X'
	if [ -f $OUTPUT_PATH$i ]; then
	    mv $INPUT_PLAYBOY_PATH$i $PROC_PATH
	fi
    fi
done

for i in `ls -1 $INPUT_PATH_OLD_TURNER`
do
    if [ -f $INPUT_PATH_OLD_TURNER$i ]; then
	echo $i
	python /opt/packager/app/python-stl-ebu/adjusttc.py -i $INPUT_PATH_OLD_TURNER$i -o $OUTPUT_PATH$i -a '00:00:05;00' -n 2 -f -p '8X' -c 
	if [ -f $OUTPUT_PATH$i ]; then
	    mv $INPUT_PATH_OLD_TURNER$i $TURNER_PROC_PATH
	fi
    fi
done
