#!/bin/bash
echo "##########################################################"
echo "# Fancontrol Workaround"
echo "# Made for Dell Inspiron 3421 using Ubuntu 18.10 on 1/3/19"
echo "##########################################################"
echo
echo "+ (1/3): Detecting sensors changing..."
OLDDEV=`cat /etc/fancontrol | grep "DEVPATH" | tail -c +9 | head -c -2`
NEWDEV=`ls /sys/devices/virtual/hwmon/hwmon*/pwm1 | tail -c +28 | head -c -6`
echo "+ (2/3): Changing Fancontrol configuration..."
sed -i s/$OLDDEV/$NEWDEV/g /etc/fancontrol
echo "+ (3/3): Restarting Fancontrol service..."
systemctl restart fancontrol
echo
echo "Fancontrol Service Status"
systemctl status fancontrol
echo
echo "### Fancontrol workaround applying has finished. ###"
echo "### In order to successfully applied this workaround, it should be no any error appear. ###"
echo
exit
