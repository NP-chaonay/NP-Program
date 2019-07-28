#!/bin/bash

read -d '\' -t 1.5

clear
read -s -d '\' -t 1.5

echo "Changing working directory..."
echo ">> cd ~/../np-chaonay/Applications/Scripts/"
cd ~/../np-chaonay/Applications/Scripts/
clear

echo "Optimizing power usage..."
echo ">> sudo -H ./PowerManagement/Launcher.sh"
sudo -H ./PowerManagement/Launcher.sh
clear

echo "Tweaking performance..."
echo ">> sudo -H ./PerformanceTweak.sh"
sudo -H ./PerformanceTweak.sh
clear

echo "Loading Pulseaudio plugins..."
echo ">> ./Pulseaudio-LoadModule-CorkOrDucking.sh"
./Pulseaudio-LoadModule-CorkOrDucking.sh
clear

echo "Starting Low Memory Alerting script..."
echo ">> killall MemAlert.sh"
killall MemAlert.sh
echo ">> ./LoopScripts/MemAlert.sh &"
./LoopScripts/MemAlert.sh &
clear

echo "Checking and updating installed packages..."
echo ">> sudo -H apt full-upgrade"
sudo -H apt full-upgrade
clear

echo "Starting Google Chrome"
echo ">> env PULSE_PROP="media.role=animation" google-chrome 2> /dev/null &"
env PULSE_PROP="media.role=animation" google-chrome 2> /dev/null &
clear

read -s -d '\' -t 1
echo "On-Startup script finished its operations."
read -s -d '\' -t 1.5
