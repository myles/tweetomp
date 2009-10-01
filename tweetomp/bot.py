import logging

import twitter

log = logging.getLogger('tweetomp.bot')

class TweetBot(object):
	def __init__(self, username, password, commands):
		self.username = username
		self.password = password
		self.commands = commands
		
		self.api = twitter.Api(self.username, self.password)
	
	def get_directs(self):
		self.tweets = self.api.GetDirectMessages()
		
		for tweet in self.tweets:
			worked, reply = self.process(tweet.text.lower())
			if worked:
				update = "@%s %s" % (tweet.sender_screen_name, reply)
				self.api.PostUpdate(update)
				logging.info("Posted update: %s" % update)				
			
			self.api.DestroyDirectMessage(tweet.id)
	
	def process(self, tweet):
		try:
			command, args = tweet.split(' ', 0)
		except ValueError:
			command = tweet
			args = None
		
		try:
			c = self.commands[command]
		except KeyError:
			log.error("Command does not exist.")
			return False, 'Command does not exist.'
		
		try:
			mod = __import__(c, '', '', [''])
		except ImportError, e:
			log.error("Couldn't import command %r: %s" % (c, e))
			return False, "Couldn't import command %r: %s" % (c, e)
		
		if not mod.enabled():
			return False, "Module couldn't be enabled."
		
		return True, mod.run(command, args)

from optparse import OptionParser

def main():
	parser = OptionParser(usage='%prog [options]')
	parser.add_option('-u', '--username',
		action = 'store',
		dest = 'username',
		help = 'Your computers Twitter username.')
	parser.add_option('-p', '--password',
		action = 'store',
		dest = 'password',
		help = 'Your computer Twitter password.')
	parser.add_option('-v', '--verbosity', 
		action='store', 
		dest='verbosity', 
		default='1',
		type='choice', 
		choices=['0', '1', '2'],
		help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
	parser.set_defaults()
	
	options, args = parser.parse_args()
	
	level = { '0': logging.WARN, '1': logging.INFO, '2': logging.DEBUG }
	logging.basicConfig(level=level[options.verbosity], format="%(name)s: %(levelname)s: %(message)s")
	
	# TODO Currently hand coded but hopfully soon though a settings file.
	COMMANDS = {
		'ip': 'tweetomp.commands.common.ip',
	}
	
	t = TweetBot(options.username, options.password, COMMANDS)
	t.get_directs()

if __name__ == '__main__':
	main()