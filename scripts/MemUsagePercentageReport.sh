#!/bin/bash

while [ true ]; do
	clear
	export MemTotal=`cat /proc/meminfo | grep -w MemTotal | awk -F " " '{ print $2 }'`
	export MemFree=`cat /proc/meminfo | grep -w MemFree | awk -F " " '{ print $2 }'`
	export MemShared=`cat /proc/meminfo | grep -w Shmem | awk -F " " '{ print $2 }'`
	export MemBuffers=`cat /proc/meminfo | grep -w Buffers | awk -F " " '{ print $2 }'`
	export MemCachedCache=`cat /proc/meminfo | grep -w Cached | awk -F " " '{ print $2 }'`
	export MemSReclaimableCache=`cat /proc/meminfo | grep -w SReclaimable | awk -F " " '{ print $2 }'`
	export MemAvailable=`cat /proc/meminfo | grep -w MemAvailable | awk -F " " '{ print $2 }'`

	export MemUsed=`awk "BEGIN {print $MemTotal-$MemFree}"`
	export MemBusy=`awk "BEGIN {print $MemTotal-$MemAvailable}"`
	export MemCache=`awk "BEGIN {print $MemCachedCache+$MemSReclaimableCache}"`
	export MemProgram=`awk "BEGIN {print $MemTotal-$MemFree-$MemBuffers-$MemCache}"`

	export MemBusyRatio=`awk "BEGIN {print 100*($MemBusy/$MemTotal)}"`
	export MemBusyRatio=`printf %.1f%% $MemBusyRatio`
	export OptimalMemBusyRatio=`awk "BEGIN {print 100*( ( 100*( $MemBusy/$MemTotal ) )/( 100-( 100*( 196585/$MemTotal ) ) ) )}"`
	export OptimalMemBusyRatio=`printf %.1f%% $OptimalMemBusyRatio`

	### Zenity Method ###
	#zenity --title="System Resources" --window-icon=system --modal --info --text="Memory Usage (in Percentage) : $MemBusyRatio\nOptimal Memory Usage (in Percentage) : $OptimalMemBusyRatio\nRecommendation : Optimal Memory Usage shouldn't be more than 100%." --icon-name=system --no-wrap --ellipsize
	#zenity --title="System Resources" --window-icon=system --modal --info --text="[Techical Informations] (In KiB)\nMemTotal=$MemTotal\nMemUsed=$MemUsed\nMemFree=$MemFree\nMemBusy=$MemBusy\nMemAvailable=$MemAvailable\nMemProgram=$MemProgram\nMemShared=$MemShared\nMemBuffers=$MemBuffers\nMemCache=$MemCache\nMemCachedCache=$MemCachedCache\nMemSReclaimableCache=$MemSReclaimableCache" --icon-name=system --no-wrap --ellipsize

	### Console Method ###
	echo "Memory Usage (in Percentage) : $MemBusyRatio"
	echo "Optimal Memory Usage (in Percentage) : $OptimalMemBusyRatio"
	echo "Recommendation : Optimal Memory Usage shouldn't be more than 100%."
	echo
	echo "Press return for refresh."
	echo "Or else, this program will end in 30 seconds..."
	read -t 30

	if [ $? -gt 128 ]; then
		clear
		exit 0
	fi
done
