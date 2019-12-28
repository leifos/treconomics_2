#!/bin/bash

if [ "$1" != "keepdata" ]; then
    echo "You do not want to keep ANY data. The log and database will be wiped if you continue."
    echo "Maybe you just want to restart the server -- try restart_server.sh instead."
    read -p "Do you want to continue? [Y/N]" -n 1 -r
    echo

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        exit 1
    fi
fi

if [ "$1" != "keepdata" ]; then
    ./clean_start.sh $1
fi

echo Need root privileges now... be prepared to enter the sudo password.

sudo chown :www-data experiment.log
sudo chown :www-data treconomics.db
chmod 664 experiment.log
chmod 664 treconomics.db
sudo systemctl restart apache2

echo You should now be good to go.
