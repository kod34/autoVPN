#!/usr/bin/env python3

from io import BytesIO
from PIL import Image
import subprocess
import urllib.request
from urllib.parse import quote
import bs4
import os
from os import listdir
from os.path import isfile, join
import re
import sys
import zipfile

banner = '''
    _           _       __     __ ____   _   _ 
   / \   _   _ | |_  ___\ \   / /|  _ \ | \ | |
  / _ \ | | | || __|/ _ \\\\ \ / / | |_) ||  \| |
 / ___ \| |_| || |_| (_) |\ V /  |  __/ | |\  |
/_/   \_\\\\__,_| \__|\___/  \_/   |_|    |_| \_|
				by kod34
                                               
'''

print(banner)

url = 'https://www.vpnbook.com/'
pattern_usr = "<strong>(.*?)</strong>"
pattern_pass = "src=\"(.*?)\""
pattern_bundle = "href=\"/(.*?)\">"
i = 1
dict_bundles = {}
c = 1
dict_files ={}

# Create directories
os.makedirs('/tmp/pass_dumps/', exist_ok=True)
os.makedirs('/tmp/bundles/', exist_ok=True)


# Get list elements from source code
url_contents = urllib.request.urlopen(url+'/freevpn').read()
soup = bs4.BeautifulSoup(url_contents, "html.parser")
elems = soup.find_all("li")

# Get & list bundles
print("Choose a bundle\n")
for x in elems[-11:-3]:
	b = re.search(pattern_bundle, str(x)).group(1)
	dict_bundles.update({i:b})
	print("\t"+str(i)+": "+dict_bundles[i])
	i+=1
try:
	bundle_choice = input("\nBundle: ")
	bundle = dict_bundles[int(bundle_choice)]
except ValueError:
	sys.exit(1)

# Download bundle
bundle_url = url+bundle
file_name = bundle_url.split('/')[-1]
urllib.request.urlretrieve(bundle_url, '/tmp/bundles/'+file_name)

# Unzip file
directory = '/tmp/bundles/'+file_name.split('.zip')[0]+'/'
with zipfile.ZipFile('/tmp/bundles/'+file_name, 'r') as zip_ref:
	zip_ref.extractall(directory)

# Get vpn file
print("\nChoose a vpn file\n")
for f in listdir(directory):
	if isfile(join(directory, f)):
		dict_files.update({c:f})
		print("\t"+str(c)+": "+dict_files[c])
		c+=1
try:
	file_choice = input("\nVPN file: ")
	file = dict_files[int(file_choice)]
except ValueError:
	sys.exit(1)

# Get username
username = re.search(pattern_usr, str(elems[-2:][0])).group(1)
# Get second part of password png url
pass_url_2 = re.search(pattern_pass, str(elems[-2:][1])).group(1)

# Save image
pass_url = url+pass_url_2.replace(" ","%20")
pass_img = urllib.request.urlopen(pass_url).read()
with open('/tmp/pass_dumps/pass.png', 'wb') as passfile:
	passfile.write(pass_img)


##### needs more work
# # Read image
# img = cv2.imread('pass_dumps/pass.png', cv2.IMREAD_GRAYSCALE)  
# thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
# thresh = cv2.resize(thresh, (0,0), fx=2.2, fy=2.2)
# # Get password
# password = pytesseract.image_to_string(thresh, config = '--psm 6').strip()

img = Image.open('/tmp/pass_dumps/pass.png')
img.show()

try:
	password = input("\nPassword: ")
except ValueError:
    
	sys.exit(1)
# Save credentials
with open('/tmp/creds.txt', 'w') as creds:
	creds.write(username+"\n"+password)

# Launch openvpn
vpnfile = directory+file
subprocess.call(['sudo', 'openvpn', '--config', vpnfile, '--auth-user-pass', '/tmp/creds.txt'])
