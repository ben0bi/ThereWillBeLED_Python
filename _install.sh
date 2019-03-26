#!/bin/bash

echo "*** Installing LED stuff. ***"
sudo apt-get install git build-essential python-pip python3-pip python-dev python3-dev scons swig
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install
sudo python3 setup.py install
echo "*** LEDs installed. ***"
