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
import subprocess
import tempfile
import datetime

log = logging.getLogger("tweetomp.commands.macosx.isight")

def enabled():
	ok = subprocess.call('isightcapture -v', shell=True) is not OSError
	if not ok:
		log.warn("You have to download the iSight Capture utility and put it in your PATH.")

def run(command, args):
	timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
	filename = u"%s/%s%s%s" % (tempfile.gettempdir(), 'grab_', timestamp, ".png")
	subprocess.call('isightcapture -t png ' + filename, shell=True)
	
	log.info("Created the file %s" % filename)
