#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Rishi Maker'
SITENAME = 'cmlzaGk'
SITEURL = 'https://cmlzagk.github.io'

PATH = 'content'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_MAX_ITEMS = 15
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Python.org', 'http://python.org/'),
         ('FlowViewer', 'http://flowviewer.azurewebsites.net/'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/rishimaker'),
          ('github' , 'http://github.com/cmlzaGk'),
          ('linkedin' , 'https://www.linkedin.com/in/rishi-maker-74a5a713/'),)

DEFAULT_PAGINATION = 10

THEME = r'../../blog/themes/pure'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
