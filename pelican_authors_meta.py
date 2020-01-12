"""
Plugin for Pelican to add metadata to an author using a Markdown file
=====================================================================
This plugin allows you to create a new author simply by adding a
markdown file to the AUTHORS_PATH directory.
"""
import logging
import os
from os.path import exists

import markdown
from pelican import signals
from pelican.generators import Generator
from pelican.urlwrappers import Author

logger = logging.getLogger(__name__)


def add_metadata(author: Author, generator: Generator):
    authors_dir = generator.settings["AUTHORS_PATH"]
    author_file_path = os.path.join(authors_dir, f"{author.slug}.md")

    if not exists(author_file_path):
        logger.warning(f"No author file found for {author.slug} in {authors_dir} directory")
        return

    md = markdown.Markdown(extensions=['meta'])

    with open(author_file_path, 'r') as f:
        author_file = md.convert(f.read())

    setattr(author, 'description', author_file)
    for name, value in md.Meta.items():
        setattr(author, name, value[0])


def add_author_metadata(generator: Generator):
    for article in generator.articles:
        for author in article.authors:
            add_metadata(author, generator)
    for draft in generator.drafts:
        for author in draft.authors:
            add_metadata(author, generator)
    for author, _ in generator.authors:
        add_metadata(author, generator)


def register():
    signals.article_generator_finalized.connect(add_author_metadata)
