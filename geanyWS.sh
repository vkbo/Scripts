#!/bin/sh

# Source:
# https://unix.stackexchange.com/questions/246827/

socket=`xprop -root _NET_CURRENT_DESKTOP`
socket=${socket##* }

if [ "$socket" ]
then
    if [ "$DISPLAY" ]
    then
        socket="${DISPLAY%.*}-$socket"
        socket=${socket#*:}
    else
        socket="NODISPLAY-$socket"
    fi
    exec geany --socket-file "/tmp/geany_socket_$socket" "$@"
else
    exec geany "$@"
fi
