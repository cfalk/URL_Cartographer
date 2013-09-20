import urllib2

def strip_innards(raw_data):
	#Two results for "<t>Hello</t> <f>World</f>"
	###Needs to reference tags!
	return raw_data[raw_data.index(">")+1: raw_data.index("</")1]

def search_web(key_word, seed):
	orig_seed = urllib2.urlopen(seed)
	raw_data = orig_seed.read()

	#Remove anything that isn't interesting to the content of the page.
	body_data = raw_data[0: raw_data.index("/body>")+8]
	print body_data

print strip_innards("<hello>world</hello>")
search_web("something", "http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/")
