#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pelican.paginator import PaginationRule

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
    'pelican_just_table'
]

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
JTABLE_TEMPLATE = """
<table class="table">
    {% if caption %}
    <caption> {{ caption }} </caption>
    {% endif %}
    {% if th != 0 %}
    <thead>
    <tr>
        {% if ai == 1 %}
        <th> No. </th>
        {% endif %}
        {% for head in heads %}
        <th>{{ head }}</th>
        {% endfor %}
    </tr>
    </thead>
    {% endif %}
    <tbody>
        {% for body in bodies %}
        <tr>
            {% if ai == 1 %}
            <td> {{ loop.index }} </td>
            {% endif %}
            {% for entry in body %}
            <td>{{ entry }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </tbody>
</table>
"""