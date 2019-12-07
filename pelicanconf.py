#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pymdownx import emoji

AUTHOR = 'Johan Vergeer'
SITENAME = 'RedGyro.com'
SITEURL = ''

THEME = 'themes/material-kit'

PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = 'en'

USE_FOLDER_AS_CATEGORY = True

# ==================================================
# Plugins
# ==================================================

PLUGINS = [
    'pelican_gist',
    'pelican.plugins.add_css_classes',
    'boxes'
]

# ==================================================
# Markdown
# ==================================================
MARKDOWN = {
    'extensions': [
        'pymdownx.emoji',
        'pymdownx.highlight',
        'pymdownx.mark',
        'pymdownx.progressbar',
        'pymdownx.superfences',
    ],
    'extension_configs': {
        "pymdownx.emoji": {
            "emoji_index": emoji.gemoji,
            "emoji_generator": emoji.to_svg,
            "alt": "short",
            "options": {
                "attributes": {
                    "align": "absmiddle",
                    "height": "20px",
                    "width": "20px"
                },
            }
        }
    },
    'output_format': 'html5',
}

# ==================================================
# Feed generation
# ==================================================
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# ==================================================
# Jinja2
# ==================================================
JINJA_ENVIRONMENT = {
    'extensions': [
        'jinja2.ext.loopcontrols'
    ]
}

# ==================================================
# Social widget
# ==================================================
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/johanvergeer', 'Join my network'),
          ('github', 'https://github.com/johanvergeer', 'Fork me on GitHub'),
          ('stack-overflow', 'https://stackoverflow.com/users/5039579/johan-vergeer', 'Follow me on StackOverflow'),)

# ==================================================
# URLS and pagination
# ==================================================
ARTICLE_URL = 'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{category}/{slug}/index.html'

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'

YEAR_ARCHIVE_URL = 'articles/{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = 'articles/{date:%Y}/index.html'
MONTH_ARCHIVE_URL = 'articles/{date:%Y}/{date:%b}/'
MONTH_ARCHIVE_SAVE_AS = 'articles/{date:%Y}/{date:%b}/index.html'

ARTICLES_ON_HOMEPAGE = 5

PAGINATED_TEMPLATES = {
    'index': None,
    'tag': 1,
    'category': 10,
    'author': 10,
}

PAGINATION_PATTERNS = (
    (1, '{url}/', '{base_name}/index.html'),
    (2, '{url}/{number}/', '{base_name}/{number}/index.html'),
)

# ==================================================
# JTable
# ==================================================
ADD_CSS_CLASSES = {
    "table": ["table"],
    "div.admonition.danger": ["foo"]
}

ADD_CSS_CLASSES_TO_PAGE = {
}

ADD_CSS_CLASSES_TO_ARTICLE = {
    "blockquote": ["blockquote"],
}
