#!/bin/bash

sudo easy_install -m pySitools2_1.0 
sudo rm -Rf /usr/local/lib/python2.7/dist-packages/pySitools2_1.0-0.1-py2.7.egg
sudo rm -Rf ~/.local/lib/python2.7/site-packages/pySitools2_1.0-0.1-py2.7.egg
sudo python setup.py install 
