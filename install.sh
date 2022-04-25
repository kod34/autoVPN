#!/bin/bash
sudo apt install xterm
pip3 install pytesseract
sudo ln -s $(readlink -f autovpn.py) ${PATH%%:*}/autovpn
