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
            # echo "apt-get install -qq $pro >/dev/null 2>&1"
            [[ $2 -eq 0 ]] && echo -e " \e[32mOK!\e[39m"
        fi

    done
    [[ $2 -eq 1 ]] && echo -e " \e[32mOK!\e[39m"
    return 0;
}

programasBasicos="pkg-config mongodb gcc make g++ cmake git subversion"
echo -e "\e[33m[INFO]\e[39m: Instalando programas basicos: \e[36m$programasBasicos\e[39m"
instalarProgramas "$programasBasicos" 0

# Instalar FITS
echo -e -n "\e[33m[INFO]\e[39m: Instalando FITS ... "
echo -e -n "descargando ... "
wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz >/dev/null
tar -xzf cfitsio_latest.tar.gz
cd cfitsio
echo -e -n "configurando ... "
./configure
echo -e -n "make ... "
make
echo -e -n "instalando ... "
make install
echo -e "\e[32mOK!\e[39m"

# Instalar GDAL
echo -e -n "\e[33m[INFO]\e[39m: Instalando GDAL ... "
echo -e -n "descargando ... "
svn checkout https://svn.osgeo.org/gdal/trunk/gdal gdal
cd gdal
echo -e -n "configurando ... "
./configure
echo -e -n "make ... "
make
echo -e -n "instalando ... "
make install
echo -e "\e[32mOK!\e[39m"

# Instalar MapServer
echo -e -n "\e[33m[INFO]\e[39m: Instalando mapServer ... "
echo -e -n "descargando ... "
git clone https://github.com/mapserver/mapserver.git
mkdir build
cd build
echo -e -n "cmake ... "
ccmake .. -DWITH_FRIBIDI=0 -DWITH_HARFBUZZ=0 -DWITH_POSTGIS=0 -DWITH_LIBXML2=0 -DWITH_GIF=0 # -> Nota: cairo, fribidi y harfbuzz no son necesarias
echo -e -n "make ... "
make 
echo -e -n "instalando ... "
make install 
echo -e "\e[32mOK!\e[39m"

# Instalar Node
sudo apt-get install npm
sudo npm cache clean -f
sudo npm install -g n
sudo n stable

# Instalar cordova
sudo npm install -g cordova