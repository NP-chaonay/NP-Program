#!/bin/bash

rm /dev/shm/PassedTime 2> /dev/null
H=$1
M=$2
S=$3

count() {
TIME=$[ 3600*$H + 60*$M + $S ] # In seconds
H=$[ $TIME/3600 ]
M=$[ ($TIME - 3600*$H)/60 ]
S=$[ $TIME - 3600*$H - 60*$M ]

while [ true ]; do
	echo $TIME > /dev/shm/PassedTime
	clear
	echo "Passed Time : $H:$M:$S"
	read -s -d '\' -t 1
	TIME=$[ $TIME + 1 ]
	H=$[ $TIME/3600 ]
	M=$[ ($TIME - 3600*$H)/60 ]
	S=$[ $TIME - 3600*$H - 60*$M ]
done
}

error() {
                echo 'Parameter Error : Please fill parameters in this format "Hours Minutes Seconds" or without parameters to count from zero.' >&2
                exit
}

if [ "$H" == "" ]; then
	if [ "$M" == "" ]; then
		if [ "$S" == "" ]; then
			H=0
			M=0
			S=0
			count
			exit
		fi
	fi
else
	if [ "$M" != "" ]; then
                if [ "$S" != "" ]; then
                        count
			exit
                fi
        fi
fi
error
