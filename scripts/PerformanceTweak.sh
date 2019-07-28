#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run this as root..."
  exit
fi

### HDD ###
#hdparm -X70 -c1 -a16 -d1 /dev/sda
### Kernel>MemoryManagement ###
sysctl -w vm.swappiness=5
