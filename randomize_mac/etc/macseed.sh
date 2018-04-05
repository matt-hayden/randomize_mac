#! /bin/sh
# Manage a simple file that seeds random MAC generation
#
# Should be suid with appropriate permissions
#
#	get					return a 02-prefixed MAC address
#	raw					last 256 bits of seed
#	reseed				force new entropy onto the end of seed
#	set	<interface>		Set an interface to the machine random address
#
set -e
refresh_length=32 # for security reasons, this should be the length required to initialize a decent hash function
seedfile=/etc/network/seed # privilege is only needed to read and write this file
since=$(date -d '03:21' '+%s') # 3:21 AM is chosen as 'new day' (local time)

if [ -s $seedfile ]
then
	if [ $(stat -c '%Y' $seedfile) -lt $since ]
	then # stale
		head -c $refresh_length /dev/urandom >> $seedfile
		reseeded=1
	fi
else
	head -c $refresh_length /dev/urandom > $seedfile
	reseeded=1
fi

mac=$(printf '02%s' $(tail -c 6 $seedfile | hexdump -s 1 -v -e '/1 ":%02X"'))
case "$1" in
	get)	echo $mac ;;
	raw)	tail -c 32 $seedfile ;;
	reseed)	[ $reseeded ] || head -c $refresh_length /dev/urandom >> $seedfile ;;
	set)	shift
			if [ $1 ]
			then
				ifconfig "$1" hw ether "$mac"
			else
				echo 'Usage: set <interface>'
				exit 10
			fi
			;;
esac
