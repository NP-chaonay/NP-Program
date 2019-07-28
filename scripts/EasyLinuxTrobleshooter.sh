#!/bin/bash

## Define text to show about available problems groups and problems in each groups. ##
PGlist() {
	echo "Find and remember number of problems group that relates to your problem."
	echo "Press Arrow or Home-End key to scroll. Then press Ctrl+X to continue."
	echo
	echo "Problems groups :"
	echo "	1) APT Issues"
}
Plist-PG1() {
	echo "Find and remember letter of problems that relates to your problem."
	echo "Press Arrow or Home-End key to scroll. Then press Ctrl+X to continue."
	echo
	echo "Problems in "APT Issues" group :"
	echo "	a) The package lists or status file could not be parsed or opened."
	echo "	+) All possible solutions of this problems group."
	echo "		b) Delete APT lists directories (/var/lib/apt/lists) and re-update APT cache. // For APT caches issues."
}

## Define problems solutions. ##
S1() {
	O1

	echo "-> Deleting APT lists directories..."
	echo "(rm -R /var/lib/apt/lists/)"
	echo "Press y to continue..."; read -s -d 'y'
	rm -R /var/lib/apt/lists/
	echo

	echo "--> Re-updating APT caches..."
	echo "(apt update)"
	echo "Press y to continue..."; read -s -d 'y'
	apt update
	echo
}

## Define operations. ##
	## Check if it is not root. ##
O1() {
	if [ "$EUID" -ne 0 ];then
		echo "Error : Trobleshooter doesn't have root privileges."
		echo "Solution : Please run this troubleshooter as root then try again."
		exit 1
	fi
}

## Script Instructions ##
clear
echo "Easy Linux Trobleshooter"
echo "Created by NP-chaonay (Nuttapong Punpipat)"
echo "Copyright 2019, Some right reserved."
echo
echo "Press enter to continue."
read -s

clear
PGlist | nano -v -

clear
echo "Type in number of selected problems group"
read PG

clear
Plist-PG$PG | nano -v -

clear
echo "Type in number of selected problems."
read P

if [ $P == "a" ] || [ $P == "b" ]; then
	S=1
	rr=1
fi

clear
if [ $rr == 1 ]; then
	echo "Trobleshooter need root privilege to solve this problems"
	echo "Make sure that trobleshooter has run as root already before trobleshooter starts."
	echo
fi
echo "Trobleshooter will start after press y."
read -s -d 'y'
clear
S$S
echo "Trobleshooter has reach the end of operations."
