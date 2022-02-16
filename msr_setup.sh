#!/bin/bash

echo "***update***"
sudo apt-get update -y
sudo apt-get upgrade -y
pip install --upgrade pip

echo "***install python library***"
pip3 install wheel
pip3 install grpcio==1.40.0
pip3 install numpy==1.21.0
pip3 install pandas
sudo apt-get install portaudio19-dev
pip3 install pyaudio
sudo apt-get install python3-sdl2
pip3 install pygame
pip3 install tweepy==3.10.0
pip3 install konlpy
pip3 install google-cloud-speech
pip3 install ibm-watson

echo "***reboot***"
sudo reboot

exit 0
