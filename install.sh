#!/bin/bash
pip3 install -r requirements.txt
sudo cp $(readlink -f autovpn.py) ${PATH%%:*}/autovpn
