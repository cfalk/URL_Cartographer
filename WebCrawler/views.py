from django.http import HttpResponse
from django.shortcuts import render

import requests
import time
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
     break

class URLMap(object):
 def __init__(self, url, depth):
  self.root_url = url
  self.url_count = dict()
  self.edge_map = dict()
  self.max_edges = 50

  #Cap the max_depth at 10 (default=2).
  self.max_depth = depth if (0 <= depth <= 10) else 2

 #Mark that the URL was encountered.
 def count_url(self, url):
  try:
   self.url_count[url]+=1 
  except:
   self.url_count[url]=1

 #Store the nodes that can be reached from a given URL.
 def mark_edge(self, start_url, end_url):
  try:
   self.edge_map[start_url].add(end_url)
  except:
   self.edge_map[start_url]={end_url}

 #Make sure edges are not already added (ie: that a loop does not exist).
  #TRUE === A loop does NOT exist and the edge is valid.
  #FALSE === A loop has occurred as the edge already exists.
 def unique_edge(self, start_url, end_url):
  try:
   return end_url not in self.edge_map[start_url]
  except:
   return True

 #All-in-one Function to add a URL to the map.
 def add_url(self, start_url, end_url):
  try:
   self.count_url(end_url)
   self.mark_edge(start_url, end_url)
  except Exception as e:
   print "Could not add URL."

 #Check that the size of the edge_map does not exceed max_edges.
 def check_size(self):
  return len(self.edge_map) <= self.max_edges

 #Return the total number of URLs found.
 def sum_url_count(self):
  return sum(self.url_count.values())

#Format the URL.
def parse_link(url):
 #Remove the "index.html" from the web address. (TODO: Is this inaccurate?) 
 url = url.replace("index.html","")

 #Remove double-slashes that may occur.
 url = url.replace("//","/")
 url = url.replace(":/","://") #Needed for the http:// or https:// header.

 #Append a "/" on the end of the URL if it is missing.
 if (url[-4:] in {".com",".gov",".org",".net",".edu"} or 
     url[-3:] in {".io", ".nr", ".uk", ".us"}):
  url = url+"/"
 #Remove GET request information that may pop up.
 if "?" in url:
  url = url[:url.index("?")]
  
 return url

#Get the main domain from the URL.
def get_domain(url):
 #Clean up the url.
 url = parse_link(url)

 #Take off any trailing bits after the third forward slash.
 #eg: "http://example.com/..."
 url_parts = url.split("/")
 domain = "{}//{}/".format(url_parts[0],url_parts[2])
 return domain

def make_map_from_url(url, url_map, domain, depth):
 try:
  #Get the response from the URL.
  url = parse_link(url)
  response = requests.get(url, timeout=0.2)

  #Strip out links from the HTTP response.
  links = StripLinks()
  links.feed(response.text)

  for link in links.data:
   #Add the HTTP/HTTPS head (and domain) if it is missing.
   if not (link[:7]=="http://" or link[:8]=="https://"):
    link = "{}{}".format(domain, link)
   else:
    domain = get_domain(link)
   link = parse_link(link)
   
   #if url_map.unique_edge(url, link) and url_map.check_size():
   if url_map.check_size():
    #Add the link to the map.
    url_map.add_url(url, link)
    #If the max_depth will be exceeded, don't map any deeper.
    if depth < url_map.max_depth:
     make_map_from_url(link, url_map, domain, depth+1)

 except Exception as e:
  url_map.add_url(url, "DEADLINK")

def home(request):
 depth_range = range(0,11)
 if request.method=="POST":
  root_url = request.POST.get("url")
  max_depth = int(request.POST.get("depth"))

  #Time how long the make_map takes.
  t0 = time.time()

  #Construct the Map.
  Map = URLMap(root_url, max_depth)
  make_map_from_url(root_url, Map, get_domain(root_url), 0)

  time_taken = time.time() - t0

  return render(request, "main.html", {
   "url":Map.root_url,
   "depth":Map.max_depth,
   "quantity":Map.url_count,
   "total_urls":Map.sum_url_count(),
   "edges":Map.edge_map,
   "time":time_taken,
   "depth_range": depth_range
   })
 return render(request, "main.html", {
  "depth_range": depth_range
  })
