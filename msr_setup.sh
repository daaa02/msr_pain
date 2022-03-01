#!/bin/bash

echo "***UPDATE***"
sudo apt-get update -y
sudo apt-get upgrade -y

echo "***INSTALL VENV***"
cd
sudo apt-get install python3-dev python3-venv
python3 -m venv venv
rm -rf ~/.cache/pip
venv/bin/python -m pip install --upgrade pip setuptools wheel
source venv/bin/activate

echo "***INSTALL PYTHON LIBRARY***"
sudo apt-get update -y
sudo apt-get upgrade -y

pip3 install wheel
pip3 install pandas
pip3 install grpcio==1.40.0 -y
pip3 install numpy==1.21.0
pip3 install tweepy==3.10.0
pip install grpcio==1.40.0
sudo pip3 install -U grpcio --no-binary=grpcio
sudo pip3 install -U grpcio-tools --no-binary=grpcio-tools

sudo apt-get install default-jdk -y
pip3 install konlpy

sudo apt-get install python3-sdl2 -y
sudo apt-get install portaudio19-dev libffi-dev libssl-dev -y
pip3 install pyaudio
pip3 install pygame
sudo apt-get install omxplayer

echo "***INSTALL IBM WATSON ASSISTANT***"
pip3 install ibm-watson

echo "***INSTALL GOOGLE SPEECH-TO-TEXT***"
sudo pip3 install --upgrade google-api-python-client
pip3 install --upgrade google-cloud-storage
pip3 install --upgrade google-cloud-speech

curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-369.0.0-linux-x86.tar.gz
tar -zxvf google-cloud-sdk-369.0.0-linux-x86.tar.gz
./google-cloud-sdk/install.sh

echo "***REBOOT && NEED TO START NEW SHELL***"
echo "***DO 'gcloud init' && CONFIGURE***"
sudo reboot now

exit 0
