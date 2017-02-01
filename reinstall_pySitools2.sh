#!/bin/bash

source ~/.bashrc

python_version=$(python --version 2>&1| awk '{print $2}' |awk -F. '{print $1}')

if [ $python_version = "2" ]
then
	pip_cmd='pip'
else
	pip_cmd='pip3'
fi

#New 24-01-2017 Avoid easy_install issue repported by A.Beeeleme 
#sudo pip uninstall -y pySitools2-1.0
sudo -H $pip_cmd install --upgrade .
