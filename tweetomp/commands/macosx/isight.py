"""Cature what the iSight camera is seeing."""

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
