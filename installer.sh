#!/bin/bash

# Effacer l'écran
clear

# Installer argparse
sudo pip3 install argparse
echo "#################### argparse installé ####################"

# Installer sounddevice
sudo pip3 install sounddevice
echo "#################### sounddevice installé ####################"

# Installer vosk
sudo pip3 install vosk
echo "#################### vosk installé ####################"

# Installer colorama
sudo pip3 install colorama
echo "#################### colorama installé ####################"

# Installer gtts
sudo pip3 install gtts
echo "#################### gtts installé ####################"

# Installer requests
sudo pip3 install requests
echo "#################### requests installé ####################"

# Installer bs4
sudo pip3 install bs4
echo "#################### bs4 installé ####################"

# Installer SimConnect (si applicable pour Linux)
sudo pip3 install SimConnect
echo "#################### SimConnect installé ####################"

sudo pip3 pip install pygame
echo "#################### pygame installé ####################"


echo "Programme terminé, les librairies ont dû s'installer avec succès"

# Pause (simulée en bash)
read -p "Appuyez sur [Enter] pour continuer..."

chmod +r Sounds/debut.wav

chmod +r Sounds/collation.wav