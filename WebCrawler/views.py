from django.http import HttpResponse
from django.shortcuts import render

import requests
from HTMLParser import HTMLParser

#Overload the HTMLParser methods.
class StripLinks(HTMLParser):
 def __init__(self):
  HTMLParser.__init__(self)
  self.data = []
 def handle_starttag(self, tag, attrs):
  if tag=="a":
   for (attr, val) in attrs:
    if attr=="href":
     if val not in "//#": #Blacklist
      self.data.append(val)
      print self.data
     break

class URLMap(object):
 def __init__(self, root_url):
  self.root_url = root_url
  self.url_count = dict()
  self.edge_map = dict()
 #Mark that the URL was encountered.
 def count_url(self, url):
  try:
   self.url_count[url]+=1 
  except:
   self.url_count[url]=1
 #Store the nodes that can be reached from a given URL.
 def mark_edge(start_url, end_url):
  try:
   self.edge_map[start_url].add(end_url)
  except:
   self.edge_map[start_url]={end_url}
 #Make sure edges are not already added (ie: that a loop does not exist).
  #TRUE === A loop does NOT exist and the edge is valid.
  #FALSE === A loop has occurred as the edge already exists.
 def unique_edge(start_url, end_url):
  try:
   return end_url not in self.edge_map[start_url]
  except:
   return True
 #All-in-one Function to add a URL to the map.
 def add_url(start_url, end_url):
  try:
   assert self.unique_edge(start_url, end_url)
   self.count_url(end_url)
   self.mark_edge(start_url, end_url)
  except Exception as e:
   print e

def make_map_from_url(url, url_map):
 try:
  if len(url_map.edge_map) < 100:
   response = requests.get(url)
   link_stripper = StripLinks()
   links = link_stripper.feed(response.text)
   print links.data
   for link in links.data:
    url_map.add_url(url, link)
    make_map_from_url(link, url_map)
  else:
   print "Finished making map!"
 except Exception as e:
  print e

def home(request):
 if request.method=="POST":
  root_url = request.POST.get("url")

  #Construct the Map.
  Map = URLMap(root_url)
  make_map_from_url(root_url, Map)
 
  return render(request, "main.html", {
   "url":Map.root_url,
   "quantity":Map.url_count,
   "edges":Map.edge_map,
   })
 return render(request, "main.html")
