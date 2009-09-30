import logging
import os.path
import glob

log = logging.getLogger('tweetomp.commands')

def expand_star(command_name):
	"""
	Expand something like 'tweetomp.commands.common.*' into a list of all the modules
	there.
	"""
	expanded = []
	command_dir = os.path.dirname(__import__(command_name[:-2], {}, {}, ['']).__file__)
	
	for f in glob.glob1(command_dir, "[!_]*.py"):
		expanded.append('%s.%s' % (command_name[:-2], f[:-3]))
	
	return expanded