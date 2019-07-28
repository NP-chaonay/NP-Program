#!/bin/bash

export PULSE_PROP="media.role=event"
rm /dev/shm/RemainingTime 2> /dev/null
H=$1
M=$2
S=$3

if [ "$H" == "" ]; then
		echo 'Parameter Error : Please fill parameters in this format "Hours Minutes Seconds"' >&2
		exit
fi
if [ "$M" == "" ]; then
                echo 'Parameter Error : Please fill parameters in this format "Hours Minutes Seconds"' >&2
                exit
fi
if [ "$S" == "" ]; then
                echo 'Parameter Error : Please fill parameters in this format "Hours Minutes Seconds"' >&2
                exit
fi


TIME=$[ 3600*$H + 60*$M + $S ] # In seconds
H=$[ $TIME/3600 ]
M=$[ ($TIME - 3600*$H)/60 ]
S=$[ $TIME - 3600*$H - 60*$M ]

while [ true ]; do
	echo $TIME > /dev/shm/RemainingTime
	clear
	if [ $TIME -le 0 ]; then
		echo "Time's UP!"
		while [ true ]; do
			paplay "/usr/share/sounds/Yaru/stereo/desktop-login.oga"
		done
	fi
	echo "Remaining Time : $H:$M:$S"
	read -t 1
	TIME=$[ $TIME - 1 ]
	H=$[ $TIME/3600 ]
	M=$[ ($TIME - 3600*$H)/60 ]
	S=$[ $TIME - 3600*$H - 60*$M ]
done
