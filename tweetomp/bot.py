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

import sys
import logging
import ConfigParser
from optparse import OptionParser

import tweepy

__project_name__ = "Tweetomp"
__project_version__ = "0.1"
__project_url__ = "http://github.com/myles/tweetomp"

log = logging.getLogger('tweetomp.bot')

class TweetBot(object):
	def __init__(self, consumer_key, consumer_secret, access_key, access_secret, commands):
		self.commands = commands
		
		self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		self.auth.set_access_token(access_key, access_secret)
		self.api = tweepy.API(self.auth)
	
	def get_directs(self):
		log.debug("Checking for direct messages.")
		self.tweets = self.api.direct_messages()
		log.debug("Got %s direct messages." % len(self.tweets))
		
		for tweet in self.tweets:
			worked, reply = self.process(tweet.text.lower())
			if worked:
				update = "@%s %s" % (tweet.sender_screen_name, reply)
				self.api.update_status(update)
				log.info("Posted update: %s" % update)				
			
			self.api.destroy_direct_message(tweet.id)
	
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
	
	try:
		log_file = config.get('tweetomp', 'log_file')
	except ConfigParser.NoOptionError:
		log_file = None
	
	logging.basicConfig(
		level = level[config.get('tweetomp', 'verbosity')],
		format="%(asctime)s: %(name)s: %(levelname)s: %(message)s",
		filename=log_file)
	
	twitter_consumer_key = config.get('twitter', 'consumer_key', None)
	twitter_consumer_secret = config.get('twitter', 'consumer_secret', None)
	
	if not twitter_consumer_key and not twitter_consumer_secret:
		print "Please register this application at <http://twitter.com/oauth_clients>."
		print "Then fill in the information in the configuration file."
		return sys.exit()
	
	twitter_access_key = config.get('twitter', 'access_key', None)
	twitter_access_secret = config.get('twitter', 'access_secret', None)
	
	if not twitter_access_key and not twitter_access_secret:
		auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
		auth_url = auth.get_authorization_url()
		print 'Please authorize: %s' % auth_url
		verifier = raw_input('PIN: ').strip()
		auth.get_access_token(verifier)
		print "access_key = %s" % auth.access_token.key
		print "access_secret = %s" % auth.access_token.secret
		return sys.exit()
	
	t = TweetBot(
		twitter_consumer_key,
		twitter_consumer_secret,
		twitter_access_key,
		twitter_access_secret,
		commands = dict(config.items('commands')))
	t.get_directs()

if __name__ == '__main__':
	main()