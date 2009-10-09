Installation
============

The easiest way to install Tweetomp is using virtualenv_.

::
	
	myles ~/tweetomp$ virtualenv .
	myles ~/tweetomp$ . bin/activate
	myles ~/tweetomp$ easy_install pip
	myles ~/tweetomp$ pip install -r requirements.txt
	myles ~/tweetomp$ python setup.py build
	myles ~/tweetomp$ python setup.py install
	myles ~/tweetomp$ ./bin/tweetomp -c config_file.cfg

If you would like to create a cron job script do this:

::
	
	#!/bin/sh
	. /home/myles/tweetomp/bin/activate
	/home/myles/tweetomp/bin/tweetomp -c config_file.cfg
	deactivate

and add this to your crontab:

::
	
	5 * * * * /home/myles/bin/tweetomp.sh

.. _virtualenv: http://pypi.python.org/pypi/virtualenv