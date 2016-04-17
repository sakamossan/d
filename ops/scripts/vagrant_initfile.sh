#!/usr/bin/env bash

set -eu


: "update apt" && {
    sudo apt-get update
    sudo apt-get install -y \
        build-essential openssl libssl-dev libssl-doc \
        libreadline6 libreadline6-dev \
        bzip2 bash sqlite3 libsqlite3-dev \
        python-dev python-pip python-pycurl \
        nginx supervisor jq cpanminus emacs \
        ntp htop git
}

: "lang and locale" && {
    sudo apt-get install -y language-pack-ja-base language-pack-ja
    sudo /usr/sbin/update-locale LANG=ja_JP.UTF-8 LANGUAGE="ja_JP:ja"
    source /etc/default/locale
    echo $LANG

    sudo cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
    sudo sh -c 'echo "Asia/Tokyo" > /etc/timezone'
    sudo dpkg-reconfigure -f noninteractive tzdata
}

: "user" && {
    sudo groupadd -g 500 mcsk
    sudo useradd -m -p '!!' -s '/bin/bash' --gid 500 --uid 500 mcsk
    sudo usermod -G adm mcsk
    sudo mkdir -p /mcsk/
    sudo chown mcsk:mcsk -R /mcsk
}

: "files2" && {
    sudo rm -rf /tmp/files2
    url=`cat url`
    sudo su - mcsk sh -c "cd /tmp; git clone ${url} files2"
}

: "login $ ssh -i ~/.ssh/mcsk_rsa -vv mcsk@192.168.33.154" && {
    sudo mkdir /home/mcsk/.ssh
    sudo chmod 700 /home/mcsk/.ssh
    sudo cp /tmp/files2/authorized_keys /home/mcsk/.ssh/authorized_keys
    sudo chmod 600 /home/mcsk/.ssh/authorized_keys
    sudo chown mcsk:mcsk -R /home/mcsk/.ssh
    sudo sh -c "cat >> /etc/sudoers<<'EOF';
%mcsk ALL=(ALL) NOPASSWD:ALL
EOF"
}

: "python" && {
    sudo su - mcsk sh -c "git clone https://github.com/yyuu/pyenv.git ~/.pyenv"
    sudo su - mcsk sh -c "~/.pyenv/bin/pyenv install 2.7.10"
    sudo su - mcsk sh -c "~/.pyenv/bin/pyenv global 2.7.10"
    sudo su - mcsk sh -c "~/.pyenv/bin/pyenv exec pip install --upgrade pip"
}

: "project" && {
    sudo su - mcsk sh -c "mkdir -p /mcsk/d/{run,log,bin}"
    sudo su - mcsk sh -c "cd /mcsk/d; git clone https://github.com/sakamossan/d.git"
    sudo su - mcsk sh -c "cd /mcsk/d/d/; git checkout deploy"
    sudo su - mcsk sh -c "cp /tmp/files2/setting_secret.py /mcsk/d/d/setting_secret.py"
    sudo su - mcsk sh -c "cd /mcsk/d/d; ~/.pyenv/bin/pyenv exec pip install -r requirements.txt"
    sudo su - mcsk sh -c "cd /mcsk/d/d; ~/.pyenv/bin/pyenv exec python ./manage.py migrate"
    sudo su - mcsk sh -c "cd /mcsk/d/d; ~/.pyenv/bin/pyenv exec python ./manage.py recreate_view"
    sudo su - mcsk sh -c "cd /mcsk/d/d; ~/.pyenv/bin/pyenv exec python ./manage.py loaddata /tmp/files2/user.json"
    sudo su - mcsk sh -c "cd /mcsk/d/d; ~/.pyenv/bin/pyenv exec python ./manage.py loaddata ./ops/files/fixtures/scrape_shop.json"
    sudo cp /mcsk/d/d/ops/files/crontab /etc/cron.d/every5minutes
    sudo su - mcsk sh -c "/mcsk/d/d/ops/files/run_d.sh"
}

: "redash" && {
    # apt-get dist-upgrade `-y`  $ we usually do not expect interactivity to bootstrap.sh
    wget "https://gist.githubusercontent.com/sakamossan/ea7a6f9ae29980234b830b85a76be952/raw/38323f77fc35577eac9198aa9b814e28ebec2120/bootstrap.sh"
    chmod +x bootstrap.sh
    ./bootstrap.sh
    sudo pip install -U redis  # https://github.com/getredash/redash/issues/946
    sudo supervisorctl restart redash_server
}
