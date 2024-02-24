# Installation OpenCVE Documentation
I made the installation on Debian. But tested it with Redhat and Ubuntu too.
It doesn't need much power:

 - 4 GB Ram
 - 40 GB Storage
 - 4 Cores

# How does OpenCVE work
OpenCVE uses the JSON feed provided by the NVD to update the local list of CVEs.
After an initial import, a background task is regulary executed to synchronize the local copy with the NVD feed. If a new CVE is added, or if a change is detected, the subscribers of the related vendors and products are alerted.

![enter image description here](https://docs.opencve.io/images/how-it-works.png)


# Installation with Docker
Get the OpenCVE docker repository:

    git clone https://github.com/opencve/opencve-docker.git
    cd opencve-docker
    cp ./conf/opencve.cfg.example ./conf/opencve.cfg

The following information has been adjusted in opencve.cfg

 - server_name changed to reversed DNS
 - POSTGRES_PASSWORD
 
Please note. The Postgres password change must also be recorded in .env! It must also be noted that the **URI in opencve also changes.**

## Initialize the stack

You can now build the OpenCVE image:

    docker-compose build
    docker-compose up -d postgres redis webserver celery_worker

## Initialize the database

    docker exec -it webserver opencve upgrade-db

## Import the data

The data is downloaded from NVD. They are updated daily.

    docker exec -it webserver opencve import-data

## Create an admin

For OpenCVE we need an Admin to customize some filters. For that we can use:

    docker exec -it webserver opencve create-user john john.doe@example.com --admin 
    Password:
    Repeat for confirmation: 
    [*] User john created.

## Start the beat

The last step is to start the scheduler:

    docker-compose up -d celery_beat


# Troubleshooting

Confirm the config above. If you you forget to change the password in env you have to stop all docker container and restart them after you loaded the config. 

# Automated Notifications with NFTY
For notifications i installed NFTY with the IOS app and connected the server with my phone. I will get an automated alarm if a CVE landed in Reports. =<9 with vendors in our Company.

# Installation NTFY

    sudo  mkdir  -p  /etc/apt/keyrings 
    curl  -fsSL https://archive.heckel.io/apt/pubkey.txt  |  sudo  gpg  -- dearmor  -o  /etc/apt/keyrings/archive.heckel.io.gpg 
    sudo  apt  install  apt-transport-https 
    sudo  sh  -c  "echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/archive.heckel.io.gpg] https://archive.heckel.io/apt debian main' \
    > /etc/apt/sources.list.d/archive.heckel.io.list"  
    sudo  apt  update 
    sudo  apt  install  ntfy 
    sudo  systemctl  enable  ntfy 
    sudo  systemctl  start  ntfy

# For notifications with IOS

Under server.yml (in bin/ntfy) change the base-upstream-url to the serverip and base-url to webserver. Without it you dont get a notification on your homescreen from ntfy.

# Create a channel for Notifications
Click on the website on create notification and name it. In my example i named it RestAPI

# Code for Cronejob
Created a pythonscript for a cronjeob so it can make 3 checks for new reports on openCVE.
