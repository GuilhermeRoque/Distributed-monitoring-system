#!/bin/bash
sudo -v
LIB=/usr/lib/python3/dist-packages
BIN=/usr/sbin
SERV=/etc/systemd/system
DATA=/var/lib/station
printf "\nInstalling dependencies into '$LIB/'...\n"
sudo pip3 install --target $LIB -r requirements.txt
printf "\nCopying lib's to '$LIB/'...\n"
sudo cp -r  driver/lib/* $LIB/
sudo cp -r interface/lib/* $LIB/
printf "\nCopying main's to '$BIN/'...\n"
sudo cp -r  driver/bin/* $BIN/
sudo cp -r interface/bin/* $BIN/
printf "\nAdding main's permissions...\n"
sudo chmod +x $BIN/mainDriver.py
sudo chmod +x $BIN/mainPublisherAMQP.py
sudo chmod +x $BIN/mainConsumerAMQP.py
sudo chmod +x $BIN/mainWeb.py
printf "\nCopying service files...\n"
sudo cp service/* $SERV/
printf "\nAdding ExecStart's...\n"
printf "\nExecStart=$BIN/mainDriver.py\n" >> $SERV/sensorDriver.service
printf "\nExecStart=$BIN/mainWeb.py\n" >> $SERV/webApp.service
printf "\nExecStart=$BIN/mainConsumerAMQP.py\n" >> $SERV/consumerAMQP.service
printf "\nExecStart=$BIN/mainPublisherAMQP.py\n" >> $SERV/publisherAMQP.service
printf "\nAdding database folder '$DATA/'...\n"
sudo mkdir $DATA
#printf "\nAdding permission to services start in system booting...\n"
#sudo systemctl enable sensorDriver.service
#sudo systemctl enable webApp.service
#sudo systemctl enable consumerAMQP.service
#sudo systemctl enable publisherAMQP.service
