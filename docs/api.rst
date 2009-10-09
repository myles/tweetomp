API
===

.. index:: API

Command
-------

.. index:: Command API

Upload
------

.. index:: Upload API

Short URL
---------

.. index:: Short URL API

To create a custom short url client your will require two functions
(1) a ``enabled``, to check and see if the plugin can run and (2) a
``shorturl`` which creates the tiny urls. It should return ``True``.

::
	
	def enabled():
		"""
		This will run before the shorturl to check and see if the 
		envourment is ready. It should return ``True`` on success and
		``False`` on failure.
		"""
	
	def shorturl(url):
		"""
		This will create your shorturl. If it was sucessful it should
		return ``True`` and the shorten URL and if failur it should
		return ``False`` and the reason it failed.
		"""
