#!/bin/bash

# Funcion para instalar programas
#   $1: lista de programas en una cadena de texto separados por espacios
#   $2: 0 = Instalacion de programas 
#       1 = Instalacion de librerias
function instalarProgramas {
    [[ $2 -eq 1 ]] && echo -n -e "\e[33m[INFO]\e[39m: Instalando librerias ... "
    for pro in $1 ; do
        dpkg -s $pro >/dev/null 2>&1
        if [[ $? -eq 1 ]]
        then
            [[ $2 -eq 0 ]] && echo -n -e "\e[33m[INFO]\e[39m: Instalando '\e[36m$pro\e[39m' ... "
            apt-get install -qq $pro >/dev/null 2>&1
            [[ $2 -eq 0 ]] && echo -e " \e[32mOK!\e[39m"
        fi

    done
    [[ $2 -eq 1 ]] && echo -e " \e[32mOK!\e[39m";
}

function error_handler {
    echo -e "\e[31mERROR!\e[39m"
}

# Checks if launched with ROOT permissions, if not, stops
if [ "$EUID" -ne 0 ]
  then echo -e "\e[31m[ERROR]\e[39m Script must be launched with ROOT permissions (try !!)"
  exit
fi

programasBasicos="pkg-config mongodb gcc make g++ cmake git subversion npm"
echo -e "\e[33m[INFO]\e[39m: Instalando programas basicos: \e[36m$programasBasicos\e[39m"
instalarProgramas "$programasBasicos" 0

# Instalar FITS

function installFITS {
    echo -e -n "\e[33m[INFO]\e[39m: Instalando FITS ... "
    echo -e -n "descargando ... "
    wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz >/dev/null 2>&1
    tar -xzf cfitsio_latest.tar.gz >/dev/null >/dev/null 2>&1
    cd cfitsio || return 10
    echo -e -n "configurando ... "
    ./configure >/dev/null >/dev/null 2>&1 || return 11
    echo -e -n "make ... "
    make >/dev/null >/dev/null 2>&1 || return 12
    echo -e -n "instalando ... "
    make install >/dev/null >/dev/null 2>&1 || return 13
}

installFITS  && echo -e "\e[32mOK!\e[39m" || error_handler $?

# Instalar GDAL

function installGDAL {
    echo -e -n "\e[33m[INFO]\e[39m: Instalando GDAL ... "
    echo -e -n "descargando ... "
    svn checkout https://svn.osgeo.org/gdal/trunk/gdal gdal >/dev/null || return 20
    cd gdal >/dev/null || return 21
    echo -e -n "configurando ... "
    ./configure >/dev/null || return 22
    echo -e -n "make (be patient 30-60 mins) ... "
    make >/dev/null || return 23
    echo -e -n "instalando ... "
    make install >/dev/null || return 24
}

installGDAL && echo -e "\e[32mOK!\e[39m" || error_handler $?

# Instalar MapServer

function installMapServer {
    echo -e -n "\e[33m[INFO]\e[39m: Instalando mapServer ... "
    echo -e -n "descargando ... "
    git clone https://github.com/mapserver/mapserver.git >/dev/null || return 30
    cd mapserver >/dev/null || return 31
    mkdir build >/dev/null || return 32
    cd build >/dev/null || return 33
    echo -e -n "cmake ... "
    ccmake .. -DWITH_FRIBIDI=0 -DWITH_HARFBUZZ=0 -DWITH_POSTGIS=0 -DWITH_LIBXML2=0 -DWITH_GIF=0 || return 34
    # -> Nota: cairo, fribidi y harfbuzz no son necesarias
    echo -e -n "make ... "
    make  || return 34
    echo -e -n "instalando ... "
    make install || return 35
}

programasBasicos="libpng-dev libfreetype6-dev libjpeg-dev libproj-dev libfcgi-dev libcairo2-dev cmake-curses-gui"
instalarProgramas "$programasBasicos" 1

installMapServer && echo -e "\e[32mOK!\e[39m" || error_handler $?

# Instalar Node
npm cache clean -f
npm install -g n
n stable

# Instalar cordova
npm install -g cordova
