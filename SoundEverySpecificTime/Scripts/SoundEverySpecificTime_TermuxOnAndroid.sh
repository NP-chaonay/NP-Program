#!/bin/bash

### In-Script Parameters ###
# VERBOSE=(1/0) : Enable outputing of verbose message of script operation to console.
# DEBUG=(1/0) : Enable debugging mode for easily checking script operations.

### Script Initialization ###
if [ "$VERBOSE" = 1 ] ; then echo "[INIT] Script has already loaded."; fi
if [ "$VERBOSE" = 1 ] ; then echo "[INIT] Verbose message displaying enabled."; fi
if [ "$VERBOSE" = 1 ] && [ "$DEBUG" = 1 ] ; then echo "[INIT] Debugging mode enabled."; fi
if [ "$VERBOSE" = 1 ] ; then echo "[INIT] Initialize internal variables..."; fi
H=12
Hf=0
M=0
S=1
WillResetConsole=0
GSnd=./SoundUsed/GeneralBell.wav
BbSnd=./SoundUsed/HoursStrike.wav
e1hSnd=./SoundUsed/WestmisterChimes_OnHours.wav
NA1Snd=./SoundUsed/Thai_National_Anthem_-_official_version_since_2004.ogg
NA2Snd=./SoundUsed/Thai_National_Anthem_-_US_Navy_Band.ogg
if [ "$VERBOSE" = 1 ] ; then echo "[INIT] Internal variables initialized."; fi
if [ "$VERBOSE" = 1 ] ; then echo "[INIT] Defining internal functions..."; fi

### Functions Definations ###
sync() {
	if [ "$VERBOSE" = 1 ] ; then echo "[SYNC] Synchronizing internal time variables..."; fi
	if [ "$DEBUG" != 1 ] ; then
		M=`date +%-M`
		if [ $M = 0 ]; then
			H=`date +%-I`
			Hf=`date +%-H`
		fi
	else
		M=$[ $M + $S ]
		if [ $M = 60 ]; then
			M=0
			Hf=$[ $Hf + 1 ]
			if [ $Hf = 24 ] ; then Hf=0; fi
			12hf
		fi
	fi
	if [ "$VERBOSE" = 1 ] ; then echo "[SYNC] Internal time variables synchronized."; fi
}

condition() {
	if [ "$VERBOSE" = 1 ] ; then echo "[CONDITION] Checking conditions and do corresponding actions..."; fi
	if [ $M = 0 ]; then
		if [ "$VERBOSE" = 1 ] && [ "$DEBUG" != 1 ]; then
			if [ "$WillResetConsole" = 1 ]; then
				clear
				WillResetConsole=0
			else
				WillResetConsole=1
			fi
		fi
		M=0
		playsnd $e1hSnd mute
		if [ $Hf = 8 ]; then
            playsnd $NA1Snd mute
		elif [ $Hf = 18 ]; then
            playsnd $NA2Snd mute
		fi
		hourstrike
	elif [ $M = 30 ]; then
		playsnd $GSnd duck &
		sleep 0.5
		playsnd $GSnd duck &
		sleep 0.5
		playsnd $GSnd duck
	elif [ $[ $M % 10 ] = 0 ]; then
		if [ $M -le 30 ]; then
			playsnd $GSnd duck &
			sleep 1
			playsnd $GSnd duck
		else
			playsnd $GSnd duck &
			sleep 0.5
			playsnd $GSnd duck
		fi
	fi
	if [ "$VERBOSE" = 1 ] ; then echo "[CONDITION] Conditional action done."; fi
}

hourstrike() {
	if [ "$DEBUG" != 1 ] ; then
		for (( c=1; c<=$H ; c++ )); do
			playsnd $BbSnd duck &
			sleep 2.4
		done
	else
			echo "[HOURSTRIKE@CONDITION] Hour striked for $H times."
			sleep 1
	fi
}

12hf() {
	if [ $Hf -gt 12 ]; then
		H=$[ $Hf - 12 ]
	else
		if [ $Hf != 0 ]; then
			H=$Hf
		else
			H=12
		fi
	fi
}

playsnd() {
	( play-audio $1 ) >/dev/null 2>&1
}

if [ "$VERBOSE" = 1 ] ; then echo "[INIT] Internal functions defined."; fi
if [ "$VERBOSE" = 1 ] ; then echo "[INIT] Initialization finished."; fi

if [ "$VERBOSE" = 1 ] && [ "$DEBUG" = 1 ] ; then echo; fi
if [ "$DEBUG" = 1 ] ; then echo "[DEBUG] Set the minute time."; read -e -i $M M; fi
if [ "$DEBUG" = 1 ] ; then echo "[DEBUG] Set the hour time."; read -e -i $Hf Hf; fi
if [ "$DEBUG" = 1 ] ; then echo "[DEBUG] Set step the minute is increased."; read -e -i $S S; fi

while [ true ]; do
	if [ "$VERBOSE" = 1 ] ; then echo; fi
	if [ "$VERBOSE" = 1 ] ; then echo "[MAIN] Beginning of loop."; fi
	if [ "$VERBOSE" = 1 ] && [ "$DEBUG" != 1 ] ; then echo "[MAIN] Wait for $[ 60 - `date +%-S` ] seconds to complete a minute."; fi
	if [ "$DEBUG" != 1 ] ; then sleep $[ 60 - `date +%-S` ]; fi
	if [ "$VERBOSE" = 1 ] && [ "$DEBUG" != 1 ] ; then echo "[MAIN] Finished waiting."; fi
	if [ "$DEBUG" = 1 ] ; then echo "[DEBUG] Press enter to skip to next minute."; read -s; fi
	sync
	if [ "$VERBOSE" = 1 ] || [ "$DEBUG" = 1 ] ; then echo "[INFO] Tracked internal variable for H,Hf,M values = $H:$Hf:$M"; fi
	condition
	if [ "$VERBOSE" = 1 ] ; then echo "[MAIN] End of loop."; fi
done
if [ "$VERBOSE" = 1 ] ; then echo; fi
if [ "$VERBOSE" = 1 ] ; then echo "[MAIN] Loop has exited."; fi
if [ "$VERBOSE" = 1 ] ; then echo "[MAIN] Script is going to exit..."; fi
