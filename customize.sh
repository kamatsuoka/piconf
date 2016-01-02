#!/bin/bash

# Remove swap file to save SD card, per
# http://www.ideaheap.com/2013/07/stopping-sd-card-corruption-on-a-raspberry-pi/

sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo update-rc.d dphys-swapfile remove

