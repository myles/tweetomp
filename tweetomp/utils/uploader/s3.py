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
import os.path

try:
	from boto.s3.connection import S3Connection
	from boto.exception import S3CreateError
	from boto.s3.key import Key
except ImportError:
	S3Connection = None

from tweetomp.conf import settings

log = logging.getLogger("tweetomp.utils.uploader.s3")

def enabled():
	ok = S3Connection is not None
	if not ok:
		log.warn("You need to install the Python library 'boto'.")
	
	ok = settings.AWS_ACCESS_KEY and settings.AWS_SECRET_KEY and settings.AWS_S3_BUCKET is not None
	if not ok:
		log.warn("Please add the 'AWS_ACCESS_KEY', 'AWS_SECRET_KEY', and 'AWS_S3_BUCKET' to your settings file.")
	
	return ok

def upload(filename):
	conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
	
	# Try creating the Bucket
	try:
		bucket = conn.create_bucket(settings.AWS_S3_BUCKET)
	except S3CreateError:
		bucket = conn.get_bucket(settings.AWS_S3_BUCKET)
	
	k = Key(bucket)
	k.key = os.path.basename(filename)
	k.set_contents_from_filename(filename)
	
	# TODO Return the URL of the file.