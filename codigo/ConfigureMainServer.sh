#!/bin/bash

function install_programs {
    for pro in $1 ; do
        if ! check_if_installed $pro ; then
            echo -n -e "\t- Installing '\e[36m$pro\e[39m' ... "
            apt-get install -qq $pro >/dev/null 2>&1
            echo -e "\e[32mOK!\e[39m"
        fi
    done
}

function check_if_installed {
    dpkg -s $1 >/dev/null 2>&1
    return $?
}

function error_handler {
    echo -e "\e[31mERROR!\e[39m"
}

# Checks if launched with ROOT permissions, if not, stops
if [ "$EUID" -ne 0 ]
  then echo -e "\e[31m[ERROR]\e[39m Script must be launched with ROOT permissions (try sudo !!)"
  exit
fi

programs="pkg-config mongodb gcc make g++ cmake git subversion npm postgis postgresql postgresql-contrib"
echo -e "\e[33m[INFO]\e[39m: Installing necessary programs: \e[36m$programs\e[39m"
install_programs "$programs"

libraries="libpng-dev libfreetype6-dev libjpeg-dev libproj-dev libgeos-dev libfcgi-dev libcairo2-dev libxml2-dev libgif-dev libgdal-dev libapache2-mod-fcgid"
echo -e "\e[33m[INFO]\e[39m: Installing necessary libraries: \e[36m$libraries\e[39m"
install_programs "$libraries"

# install FITS
function install_FITS {
    echo -e -n "\e[33m[INFO]\e[39m: Installing FITS ... "
    if ls /usr/lib | grep libcfitsio >/dev/null ; then
        echo -e "\e[32malready installed\e[39m"
    else
        echo -e -n "downloading ... "
        cd ~
        wget https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz >/dev/null 2>&1 || error_handler && return 10
        cd /usr/local/src
        mv ~/cfitsio_latest.tar.gz  . || error_handler && return 11
        tar -xzf cfitsio_latest.tar.gz >/dev/null >/dev/null 2>&1 || error_handler && return 12
        cd cfitsio || return 10 || error_handler && return 13
        echo -e -n "configuring ... "
        ./configure --prefix=/usr >/dev/null 2>&1 || error_handler && return 14
        echo -e -n "make ... "
        make >/dev/null 2>&1 || error_handler && return 15
        echo -e -n "installing ... "
        make install >/dev/null 2>&1 || error_handler && return 16
        make clean >/dev/null 2>&1 || error_handler && return 17
        cd
        rm -fr cfitsio_latest.tar.gz
        echo -e "\e[32mOK!\e[39m"
    fi
}

install_FITS || error_handler $?

# function install_GDAL { # can be installed from libgdal-dev without creating binaries
#     echo -e -n "\e[33m[INFO]\e[39m: Installing GDAL ... "
#     echo -e -n "downloading ... "
#     svn checkout https://svn.osgeo.org/gdal/trunk/gdal gdal >/dev/null || return 20
#     cd gdal >/dev/null || return 21
#     echo -e -n "configuring ... "
#     ./configure >/dev/null || return 22
#     echo -e -n "make (be patient 30-60 mins) ... "
#     make >/dev/null || return 23
#     echo -e -n "installing ... "
#     make install >/dev/null || return 24
# }
# install_GDAL && echo -e "\e[32mOK!\e[39m" || error_handler $?

# Install MapServer
function install_MapServer {
    echo -e -n "\e[33m[INFO]\e[39m: Installing MapServer ... "
    if which mapserv >/dev/null ; then
        echo -e "\e[32malready installed\e[39m"
    else
        echo -e -n "downloading ... "
        cd ~
        git clone https://github.com/mapserver/mapserver.git >/dev/null 2>&1 || error_handler && return 30
        cd mapserver >/dev/null || error_handler && return 31
        mkdir build >/dev/null || error_handler && return 32
        cd build >/dev/null 2>&1 || error_handler && return 33
        echo -e -n "cmake ... "
        cmake .. -DWITH_FRIBIDI=0 -DWITH_HARFBUZZ=0 >/dev/null 2>&1 || error_handler && return 34
        echo -e -n "make ... "
        make >/dev/null 2>&1 || error_handler && return 34
        echo -e -n "installing ... "
        make install >/dev/null 2>&1 || error_handler && return 35
        cd
        rm -fr mapserver
        echo -e "\e[32mOK!\e[39m"
    fi
}

install_MapServer || error_handler $?

function config_ApacheCGI {
    echo -e -n "\e[33m[INFO]\e[39m: Configuring Apache cgi ... "
    a2enmod fcgid cgi alias proxy proxy_http headers || error_handler && return 41
    ln -s /usr/bin/mapserv /usr/lib/cgi-bin/mapserv.fcgi || error_handler && return 42
    # ProxyPreserveHost On
    # ProxyPass / http://localhost:3000/
    # ProxyPassReverse / http://localhost:3000/
    # ServerName localhost
    # Header set Access-Control-Allow-Origin "*"
    echo -e "\e[32mOK!\e[39m"
}

config_ApacheCGI

# Configuring NPM
echo -e -n "\e[33m[INFO]\e[39m: Configuring NPM ... "
npm cache clean -f >/dev/null 2>&1 || error_handler && exit
npm install -g n >/dev/null 2>&1 || error_handler && exit
n stable >/dev/null 2>&1 || error_handler && exit
echo -e "\e[32mOK!\e[39m"

# Installing cordova
# echo -e -n "\e[33m[INFO]\e[39m: Installing cordova ... "
# if which cordova >/dev/null ; then
#     echo -e "\e[32mYA INSTALADO!\e[39m"
# else
#     npm install -g cordova >/dev/null 2>&1
#     echo -e "\e[32mOK!\e[39m"
# fi

# Preparing Workspace
echo -e -n "\e[33m[INFO]\e[39m: Preparing workspace ... "
git clone https://smallsignals@bitbucket.org/smallsignals/cazasteroides.git || error_handler && exit
cd cazasteroides/ || error_handler && exit
echo -e -n "moving to correct branch ... "
git checkout fusion2 || error_handler && exit
cd server/cazasteroides/ || error_handler && exit
echo -e -n "installing dependencies ... "
npm install || error_handler && exit
echo -e "\e[32mOK!\e[39m"
