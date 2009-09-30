"""Uploads a file to Amazon's S3 service."""

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