#!/usr/bin/env bash

set -eu


# update apt
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y openssh-client openssh-server

# lang and locale
sudo apt-get install -y language-pack-ja-base language-pack-ja
sudo /usr/sbin/update-locale LANG=ja_JP.UTF-8 LANGUAGE="ja_JP:ja"
source /etc/default/locale
echo $LANG

# timezone
sudo cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
sudo sh -c 'echo "Asia/Tokyo" > /etc/timezone'
sudo dpkg-reconfigure -f noninteractive tzdata

# user
sudo groupadd -g 500 mcsk
sudo useradd -m -p '!!' -s '/bin/bash' --gid 500 --uid 500 mcsk
sudo usermod -G adm mcsk
sudo mkdir -p /mcsk/
sudo chown mcsk:mcsk -R /mcsk

# files
sudo rm -rf /tmp/files2
url=`cat url`
sudo su - mcsk sh -c "cd /tmp; git clone ${url} files2"

# login $ ssh -i ~/.ssh/mcsk_rsa -vv mcsk@192.168.33.154
sudo mkdir /home/mcsk/.ssh
sudo chmod 700 /home/mcsk/.ssh
sudo cp /tmp/files2/authorized_keys /home/mcsk/.ssh/authorized_keys
sudo chmod 600 /home/mcsk/.ssh/authorized_keys
sudo chown mcsk:mcsk -R /home/mcsk/.ssh
