#!/bin/bash

BOT_ROOT=$(dirname "$0")

cd $BOT_ROOT

info=/tmp/myservice-systemd-cat-pipe-info
mkfifo "$info"
trap "exec 3>&-; rm $info" EXIT
systemd-cat -p info < "$info" &
exec 3>"$info"

DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Hammer-bot service started at ${DATE} in ${BOT_ROOT}" | systemd-cat -p info

/usr/bin/env python3 $BOT_ROOT/bot
