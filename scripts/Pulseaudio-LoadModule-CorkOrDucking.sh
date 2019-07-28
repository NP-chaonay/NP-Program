#!/bin/bash
check() {
if [ -f /run/user/100*/pulse/pid ]; then
	pactl unload-module module-role-ducking
	pactl unload-module module-role-cork
	# Ducking
	pactl load-module module-role-ducking trigger_roles=event,phone,a11y ducking_roles=video,music,game,animation,production,other volume=50%
	# Cork
	#pactl load-module module-role-cork trigger_roles=event,phone,a11y cork_roles=video,music,game,animation,production,other
else
	read -t 10
	check
fi
}

check
