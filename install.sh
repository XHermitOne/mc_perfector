# !/bin/sh

# MC
sudo apt install --assume-yes mc

# System information
sudo apt install --assume-yes neofetch

# cat analog
sudo apt install --assume-yes bat

# top analogs
sudo apt install --assume-yes htop
sudo apt install --assume-yes btop

sudo snap install bottom

# ps analog
sudo snap install procs

# du analog
sudo snap install dust

# net tools
sudo apt install --assume-yes mtr
sudo apt install --assume-yes termshark

# json viewer
sudo apt install --assume-yes jq

# log viewer
sudo apt install --assume-yes lnav

# pdftotext
sudo apt install --assume-yes poppler-utils

# HTML viewer and Internet browser
sudo apt install --assume-yes lynx

# JSON viewer
sudo snap install json-tui

# Image viewer
sudo snap install --edge tiv

# Microsoft documents viewer
sudo apt install --assume-yes catdoc
sudo apt install --assume-yes docx2txt
sudo apt install --assume-yes pandoc
sudo apt install --assume-yes xlsx2csv

# Libreoffice documents viewer
sudo apt install --assume-yes unoconv

#Git manager
sudo snap install lazygit-gm

# Internet searching
sudo snap install ddgr

# Configuration script
sudo apt install --assume-yes python3-pip
sudo apt install --assume-yes python3-dialog
sudo apt install --assume-yes python3-jinja2
sudo apt install --assume-yes python3-termcolor
pip3 install rich

mc --help

python3 ./mc_perfect_config.py
