"""Returns the external IP address."""

import logging

try:
	import urllib2
except ImportError:
	urllib2 = None

log = logging.getLogger("tweetcomp.commands.common.ip")

def enabled():
	ok = urllib2 is not None
	# TODO Add a check to see if their is an internet connection out.
	if not ok:
		log.warn("The library urllib2 is not installed.")
	
	return ok

def run():
	url = urllib2.urlopen("http://checkip.dyndns.com/")
	html = url.read()
	
	ends_with = html.find("</body></html>")
	starts_with = html.find("Current IP Address: ") + len("Current IP Address: ")
	
	return u"%s" % html[starts_with:ends_with].strip()