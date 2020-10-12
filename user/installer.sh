#!/bin/bash
sudo -v
SRC=$(python3 -m site --user-site)
BIN=/usr/local/bin/
printf "Installing dependencies into '$SRC'...\n"
sudo pip3 uninstall -r requirements.txt
sudo pip3 install --target $SRC -r requirements.txt
printf "Installing project into '$SRC'...\n"
sudo cp commands/* "$BIN"
sudo  chmod +x "$BIN"amqp-listen.py
sudo  chmod +x "$BIN"amqp-request.py