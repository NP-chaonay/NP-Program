#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run this as root..."
  exit
fi

echo -n "Press "y" to confirm hibernation or else press Ctrl+C to cancel operation..."
read -s -d 'y'
echo
#	echo "(1/4) Disable non-hibernation swaps..."
echo "(1/2) Disable non-hibernation swaps..."
swapoff /dev/zram*
#	echo "(2/4) Disable USB auto-suspending on system disks devices..."
#	echo on > /sys/devices/power/power/control
#	echo on > /sys/devices/pci0000:00/power/control
#	echo on > /sys/devices/pci0000:00/0000:00:14.0/usb4/power/control
#	for control in `find /sys/devices/pci0000:00/0000:00:14.0/usb4/4-2/ | grep -i "power/control"`
#	{
#		echo on > $control
#	}
#	echo "(3/4) Wait for system applying changes..."
#	read -s -d '\' -t 10
#	sync
#	echo "(4/4) Hibernating..."
echo "(2/2) Hibernating..."
systemctl hybrid-sleep
#systemctl hibernate
echo
echo -n "After hibernated, press enter to continue resuming."
read -s
echo
echo
#	echo "(1/2) Re-enable USB auto-suspending on system disks devices..."
#	echo auto > /sys/devices/power/power/control
#	echo auto > /sys/devices/pci0000:00/power/control
#	echo auto > /sys/devices/pci0000:00/0000:00:14.0/usb4/power/control
#	echo "(2/2) Re-enable non-hibernation swaps..."
echo "(1/1) Re-enable non-hibernation swaps..."
swapon -p 5 /dev/zram*
echo "Resumed."
