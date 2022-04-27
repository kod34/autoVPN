#!/bin/bash
pip3 install pytesseract
sudo cp $(readlink -f autovpn.py) ${PATH%%:*}/autovpn
