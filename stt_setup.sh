#!/bin/bash

echo "!!!!! install with pip version==19.2.3 !!!!!1"
echo "install with pip version==19.2.3"
echo "install with pip version==19.2.3"
echo "install with pip version==19.2.3"
echo "install with pip version==19.2.3"

echo "***INSTALL VENV***"
sudo apt-get install python3-dev python3-venv
python3 -m venv venv
rm -rf ~/.cache/pip
venv/bin/python -m pip install --upgrade pip setuptools wheel
source venv/bin/activate

echo "***INSTALL GOOGLE SPEECH-TO-TEXT***"
sudo apt-get install portaudio19-dev libffi-dev libssl-dev
pip3 install pyaudio
pip3 install --upgrade google-cloud-storage
pip3 install --upgrade google-cloud-speech

curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-369.0.0-linux-x86.tar.gz
tar -zxvf google-cloud-sdk-369.0.0-linux-x86.tar.gz
gcloud init

echo "***NEED TO START NEW SHELL***"

exit 0
