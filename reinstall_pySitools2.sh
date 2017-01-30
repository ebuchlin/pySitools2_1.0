#!/bin/bash

source ~/.bashrc

#New 24-01-2017 Avoid easy_install issue repported by A.Beeeleme 
#sudo pip uninstall -y pySitools2-1.0
sudo -H pip install --upgrade .
