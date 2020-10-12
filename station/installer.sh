#!/bin/bash
sudo -v
LIB=/usr/lib/python3/dist-packages
BIN=/usr/sbin
SERV=/etc/systemd/system
DATA=/var/lib/station
printf "\nInstalling dependencies into '$LIB/'...\n"
sudo pip3 install --target $LIB -r requirements.txt
printf "\nCopying lib's to '$LIB/'...\n"
sudo cp  driver/dht11.py $LIB/
sudo cp  driver/driver.py $LIB/
sudo cp  driver/sensor.py $LIB/
sudo cp  driver/sensorIO.py $LIB/
sudo cp  interface/amqpConn.py $LIB/
sudo cp  interface/consumerAMQP.py $LIB/
sudo cp  interface/flaskApp.py $LIB/
sudo cp  interface/publisherAMQP.py $LIB/
sudo cp  interface/zmqRequest.py $LIB/
printf "\nCopying main's to '$BIN/'...\n"
sudo cp -r  driver/mainDriver.py $BIN/
sudo cp -r interface/mainWeb.py $BIN/
sudo cp -r interface/mainPublisherAMQP.py $BIN/
sudo cp -r interface/mainConsumerAMQP.py $BIN/
printf "\nAdding main's permissions...\n"
sudo chmod +x $BIN/mainDriver.py
sudo chmod +x $BIN/mainPublisherAMQP.py
sudo chmod +x $BIN/mainConsumerAMQP.py
sudo chmod +x $BIN/mainWeb.py
printf "\nCopying service files...\n"
sudo cp service/* $SERV/
printf "\nAdding ExecStart's...\n"
sudo printf "\nExecStart=$BIN/mainDriver.py\n" >> $SERV/sensorDriver.service
sudo printf "\nExecStart=$BIN/mainWeb.py\n" >> $SERV/webApp.service
sudo printf "\nExecStart=$BIN/mainConsumerAMQP.py\n" >> $SERV/consumerAMQP.service
sudo printf "\nExecStart=$BIN/mainPublisherAMQP.py\n" >> $SERV/publisherAMQP.service
sudo printf "\nAdding database folder '$DATA/'...\n"
sudo mkdir $DATA
#printf "\nAdding permission to services start in system booting...\n"
#sudo systemctl enable sensorDriver.service
#sudo systemctl enable webApp.service
#sudo systemctl enable consumerAMQP.service
#sudo systemctl enable publisherAMQP.service
