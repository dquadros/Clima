#!/bin/bash
echo
echo Preparando ambiente
echo
sudo apt-get install build-essential python-dev python-pip
sudo apt-get install python-imaging python-smbus
sudo apt-get install i2c-tools
sudo pip install requests
echo
echo  Instalando biblioteca Adafruit DHT
echo
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
cd ..
echo
echo Instalando biblioteca Adafruit SSD1306
echo
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
cd ..
echo
echo Fazendo download das fontes
echo
wget https://dl.dafont.com/dl/?f=minecraftia -O minecraftia.zip
wget https://dl.dafont.com/dl/?f=manualdisplay -O manualdisplay.zip
unzip minecraftia.zip
unzip manualdisplay.zip
echo
echo Nao esqueca de acertar chave da API e o codigo da cidade em clima.py
