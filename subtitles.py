from sys import argv

import json
import urllib
import os
import zipfile
import sys

script, file_name = argv

def showsome(searchfor):
  query = urllib.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  hits = data['results']
  if len(hits) == 0:
	print "Oops, no results."
	return
  elif len(hits) > 0:
  	print 'Top %d hits:' % len(hits)
  	count = 0
  	for h in hits: 
  		count += 1
  		print count, '-', h['url']  
  	print "Select one:"
  	select = raw_input("> ")
  	select = int(select) - 1
  	address = str(hits[select]['url'])
  	return int(filter(str.isdigit, address))
  else:
	print "Something went catastrophically wrong."

file_size = os.path.getsize(file_name)

print "File size:"
print file_size

short_name = os.path.splitext(file_name)[0]

lang = "es"

searchie = "site:opensubtitles.org/%s/subtitles %s" % (lang, file_size)

first_id = showsome(searchie)

if first_id is None:
	print "Switching to English..."
	lang = "en"
	searchie = "site:opensubtitles.org/%s/subtitles %s" % (lang, file_size)
	print "Let's try that again."
	first_id = showsome(searchie)
	if first_id is None:
		sys.exit()
	else:
		print "Subtitles in English? Fine."
else:
	print "Great, moving on..."

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

print "Done!"