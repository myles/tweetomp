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

from tweetomp.conf import settings

def shorturl(url):
	try:
		mod = __import__(settings.TWEETOMP_SHORTURLER, '', '', [''])
	except ImportError, e:
		log.error("Couldn't import command %r: %s" % (c, e))
		return False, "Couldn't import command %r: %s" % (c, e)
	
	if not mod.enabled():
		return False, "Module couldn't be enabled."
	
	return True, mod.shorturl(url)