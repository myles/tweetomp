"""
Copyright 2009 Myles Braithwaite <me@mylesbraithwaite.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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

def run(command, args):
	url = urllib2.urlopen("http://checkip.dyndns.com/")
	html = url.read()
	
	ends_with = html.find("</body></html>")
	starts_with = html.find("Current IP Address: ") + len("Current IP Address: ")
	
	return u"my ip address is %s" % html[starts_with:ends_with].strip()