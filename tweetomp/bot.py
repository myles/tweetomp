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
import ConfigParser

def main():
	parser = OptionParser(usage='%prog [options]')
	parser.add_option('-c', '--config',
		action = 'store',
		dest = 'config_file',
		help = 'Tweetomp configuration file.')
	parser.set_defaults()
	
	options, args = parser.parse_args()
	
	config = ConfigParser.ConfigParser()
	config.read(options.config_file)
	
	level = { '0': logging.WARN, '1': logging.INFO, '2': logging.DEBUG }
	logging.basicConfig(
		level = level[config.get('tweetomp', 'verbosity')],
		format="%(name)s: %(levelname)s: %(message)s")
	
	t = TweetBot(
		username = config.get('twitter', 'username'),
		password = config.get('twitter', 'password'),
		commands = dict(config.items('commands')))
	t.get_directs()

if __name__ == '__main__':
	main()