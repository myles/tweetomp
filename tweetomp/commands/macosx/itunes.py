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
	from Foundation import *
	from ScriptingBridge import *
	import objc
except ImportError:
	objc = None

log = logging.getLogger("tweetcomp.commands.macosx.itunes")

def enabled():
	ok = objc is not None
	if not ok:
		log.warn("The PyObjC library is not installed.")
	
	return ok

def run(command, args):
	iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
	
	if not iTunes.isRunning():
		return "my iTunes is not running."
	
	try:
		return u"my iTunes is currently playing: %s by %s" % (iTunes.currentTrack().name(), iTunes.currentTrack().artist())
	except objc.error:
		return "my iTunes is open but nothing is playing."