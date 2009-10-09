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

log = logging.getLogger("tweetcomp.commands.linux.uptime")

try:
	f = open( "/proc/uptime" )
	uptime_file = f.read().split()
	f.close()
except:
	uptime_file = None

def enabled():
	ok = uptime_file is None
	if not ok:
		log.warn("Cannot open uptime file: /proc/uptime.")
	
	return ok

def run(command, args):
	total_seconds = float(uptime_file[0])
	
	MINUTE = 60
	HOUR = MINUTE * 60
	DAY = HOUR * 24
	
	days = int(total_seconds / DAY)
	hours = int((total_seconds % DAY) / HOUR)
	minutes = int((total_seconds % HOUR) / MINUTE)
	seconds = int(total_seconds % MINUTE)
	
	string = ""
	
	if days > 0:
		string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
	
	if len(string) > 0 or hours > 0:
		string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
	
	if len(string) > 0 or minutes > 0:
		string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
	
	string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
	
	return u"my uptime is: %s" % string