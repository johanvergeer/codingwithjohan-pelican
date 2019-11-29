#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Johan Vergeer'
SITENAME = 'RedGyro.com'
SITEURL = ''

THEME = 'themes/material-kit'

PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = 'en'

USE_FOLDER_AS_CATEGORY = True

# Articles
ARTICLE_URL = 'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{category}/{slug}/index.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/johanvergeer', 'Join my network'),
          ('github', 'https://github.com/johanvergeer', 'Follow me on GitHub'),
          ('stack-overflow', 'https://stackoverflow.com/users/5039579/johan-vergeer', 'Follow me on StackOverflow'),)

# Pagination
DEFAULT_PAGINATION = 1

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
