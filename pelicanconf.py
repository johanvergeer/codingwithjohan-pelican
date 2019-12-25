#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from pymdownx import emoji

AUTHOR = "Johan Vergeer"
SITENAME = "Coding With Johan"

SITEURL = ''

THEME = 'themes/material-kit'

PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = 'en'

USE_FOLDER_AS_CATEGORY = True

DEFAULT_METADATA = {
    'status': 'draft',
    'excerpt_image': '/img/1_500px.jpg',
    'banner_image': '/img/1_1000px.jpg'
}

# ==================================================
# Static
# ==================================================
STATIC_PATHS = ["img"]

# ==================================================
# Theme settings
# ==================================================

# Value of the catchphrase on the homepage banner
CATCHPHRASE = "Doing what I like, and liking what I do"
# Name of the homepage banner image
HOMEPAGE_BANNER = "/img/passion-led-us-here-2.jpg"
# Name of the favicon image
FAVICON = "/img/favicon-32.png"

# Articles
# ========
# Value of the "Read More" button on each post excerpt
READ_MORE = "Read more"

# The default image displayed on the articles list
DEFAULT_ARTICLE_EXCERPT_IMAGE = "/img/1_500px.jpg"

# The default image displayed on the article page
DEFAULT_ARTICLE_PAGE_IMAGE = ""

# ==================================================
# Plugins
# ==================================================

PLUGINS = [
    'pelican_gist',
    'pelican.plugins.add_css_classes',
    'pelican.plugins.timegraphics',
    'pelican.plugins.series',
    'pelican.plugins.simple_footnotes'
]

# ==================================================
# Markdown
# ==================================================
MARKDOWN = {
    'extensions': [
        'mk_card',
        'markdown.extensions.attr_list',
        'pymdownx.emoji',
        'pymdownx.highlight',
        'pymdownx.mark',
        'pymdownx.progressbar',
        'pymdownx.superfences',
        'footnotes',
        'toc',
        'markdown.extensions.comments'
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

DRAFT_URL = 'drafts/{slug}'
DRAFT_SAVE_AS = 'drafts/{slug}/index.html'

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
# CSS Classes
# ==================================================
ADD_CSS_CLASSES = {
    "table": ["table"],
}

ADD_CSS_CLASSES_TO_PAGE = {
}

ADD_CSS_CLASSES_TO_ARTICLE = {
    "blockquote": ["blockquote"],
}
