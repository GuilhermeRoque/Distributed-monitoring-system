#!/bin/bash
sudo -v
SRC=/usr/lib/python3/dist-packages/
printf "Installing dependencies into '$SRC'...\n"
sudo pip3 uninstall -r requirements.txt
sudo pip3 install --target $SRC -r requirements.txt
printf "Installing project into '$SRC'...\n"
sudo cp -r  driver "$SRC"
sudo cp -r interface "$SRC"
printf "Adding permissions...\n"
sudo  chmod +x "$SRC"/driver/driver.py
sudo  chmod +x "$SRC"/interface/publisher.py
sudo  chmod +x "$SRC"/interface/consumer.py
printf "Building service files...\n"
printf "\nExecStart=$SRC/driver/driver.py" >> service/sensorDriver.service
printf "\nExecStart=$SRC/interface/webApp.py" >> service/webApp.service
printf "\nExecStart=$SRC/interface/consumer.py" >> service/consumerAMQP.service
printf "\nExecStart=$SRC/interface/publisher.py" >> service/publisherAMQP.service
printf "Adding service files...\n"
sudo cp service/* /etc/systemd/system/
printf "Adding permission to services start in system booting...\n"
sudo systemctl enable sensorDriver.service
sudo systemctl enable webApp.service
sudo systemctl enable consumerAMQP.service
sudo systemctl enable publisherAMQP.service
