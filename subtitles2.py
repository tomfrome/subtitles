from sys import argv
from subconfig import languages
from google import search

import json
import urllib
import os
import zipfile
import sys

script, file_name = argv


def showsome(searchfor):
  count = 0
  listem = []
  for url in search(searchfor, stop=5):
  	count += 1
  	print count, '-', url
  	listem.append(url)
  if count == 0:
  	print "Oops, no results."
  	return
  print "Select one:"
  select = raw_input("> ")
  select = int(select) - 1
  address = str(listem[select])
  return int(filter(str.isdigit, address))


file_size = os.path.getsize(file_name)
print "File size:"
print file_size

short_name = os.path.splitext(file_name)[0]

first_id = None
number = 0

while first_id is None and number < len(languages):
	lang = languages[number]
	searchie = "site:opensubtitles.org/%s/subtitles %s" % (lang, file_size)
	first_id = showsome(searchie)
	number += 1
	
url = 'http://dl.opensubtitles.org/%s/download/sub/%s' % (lang, first_id)
 
print "Downloading..."

urllib.urlretrieve(url, "subs.zip")

print "Unzipping into Holding Cell..."

directory = "Holding Cell"

if not os.path.exists(directory):
    os.makedirs(directory)

fh = open('subs.zip', 'rb')
z = zipfile.ZipFile(fh)
for name in z.namelist():    
    z.extract(name, directory)
fh.close()

mixed_bag = os.listdir(directory)
for item in mixed_bag:
	full_path = directory + "/" + item
	if item.endswith('.nfo'):
		print "Eliminating riff-raff..."
		os.remove(full_path)
	elif item.endswith('.srt'): 
		print "Renaming and relocating subtitles..."
		new_path = short_name + '.srt'
		os.rename(full_path, new_path)
	elif item.endswith('.sub'):
		print "Renaming and relocating subtitles..."
		new_path = short_name + '.sub'
		os.rename(full_path, new_path)
	elif item == ".DS_Store":
	#I have no idea what this is but I'm gonna ignore it
		cake = 1 + 1
	else:
		print "Unexpected file discovered:"
		print item
		
print "Cleaning up..."
os.remove('subs.zip')
os.remove('subconfig.pyc')

print "Done!"
	