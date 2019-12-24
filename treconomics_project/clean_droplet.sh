#!/bin/bash

./clean_start.sh

echo Need root privileges now... be prepared to enter the sudo password.

sudo chown :www-data experiment.log
sudo chown :www-data treconomics.db
chmod 664 experiment.log
chmod 664 treconomics.db
sudo systemctl restart apache2

echo You should now be good to go.
