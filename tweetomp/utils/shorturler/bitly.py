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

import urllib2
from urllib import urlencode

try:
	import simplejson
except ImportError:
	simplejson = None

from tweetomp.conf import settings

def enabled():
	ok = simplejson is not None
	if not ok:
		log.warn("Please install the Python library simplejson.")
	
	ok = settings.BITLY_LOGIN and settings.BITLY_API_KEY is not None
	if not ok:
		log.warn("Please add the 'BITLY_LOGIN' and 'BITLY_API_KEY' to your settings file.")
	
	return ok

def shorturl(url):
	encode = urlencode({
		'version': '2.0.1',
		'longUrl': url,
		'login': settings.BITLY_LOGIN,
		'apiKey': settings.BITLY_API_KEY,
		'format': 'json'})
	
	url = urllib2.urlopen('http://api.bit.ly/shorten?%s' % encode)
	json = url.read()
	
	if json['statusCode'] == 'ERROR':
		log.warn("Bit.ly returned an error: %r %s" % (json['errorCode'], json['errorMessage']))
		return False
	elif json['statusCode'] == 'OK':
		return json['shortUrl']
	else:
		return False