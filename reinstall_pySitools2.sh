#!/bin/bash

#Old 
#sudo easy_install -m pySitools2_1.0 
#sudo rm -Rf /usr/local/lib/python2.7/dist-packages/pySitools2_1.0-0.1-py2.7.egg
#sudo rm -Rf ~/.local/lib/python2.7/site-packages/pySitools2_1.0-0.1-py2.7.egg
#sudo python setup.py install 

#New 24-01-2017 Avoid easy_install issue repported by A.Beeeleme 
sudo -H pip uninstall pySitools2_1.0
sudo -H pip install --force-reinstall . 
