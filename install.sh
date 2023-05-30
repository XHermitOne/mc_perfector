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

# Git client
sudo snap install lazygit-gm

# Configuration script
sudo apt install --assume-yes python3-pip
sudo apt install --assume-yes python3-dialog
sudo apt install --assume-yes python3-jinja2
sudo apt install --assume-yes python3-termcolor
pip3 install rich

mc --help

python3 ./mc_perfect_config.py
