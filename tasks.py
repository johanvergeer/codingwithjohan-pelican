# -*- coding: utf-8 -*-

import datetime
import os
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Optional

from invoke import task
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file
from slugify import slugify

from netlify_client import NetlifyClient
from utils import yes_or_no

PROJECT_ROOT = Path().absolute()
CONTENT_ROOT = PROJECT_ROOT / "content"

SETTINGS_FILE_BASE = "pelicanconf.py"
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    "settings_base": SETTINGS_FILE_BASE,
    "settings_publish": "publishconf.py",
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    "deploy_path": SETTINGS["OUTPUT_PATH"],
    # Github Pages configuration
    "github_pages_branch": "gh-pages",
    "commit_message": "'Publish site on {}'".format(datetime.date.today().isoformat()),
    # Port for `serve`
    "port": 8000,
}


@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])


@task
def build(c):
    """Build local version of site"""
    c.run("pelican -s {settings_base}".format(**CONFIG))


@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run("pelican -d -s {settings_base}".format(**CONFIG))


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    c.run("pelican -r -s {settings_base}".format(**CONFIG))


@task
def serve(c):
    """Serve site at http://localhost:$PORT/ (default port is 8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG["deploy_path"], ("", CONFIG["port"]), ComplexHTTPRequestHandler
    )

    sys.stderr.write("Serving on port {port} ...\n".format(**CONFIG))
    server.serve_forever()


@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


@task
def preview(c):
    """Build production version of site"""
    c.run("pelican -s {settings_publish}".format(**CONFIG))


@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    build(c)
    server = Server()

    # Watch the base settings file
    server.watch(CONFIG["settings_base"], lambda: build(c))
    # Watch content source files
    content_file_extensions = [".md", ".rst", ".bib"]
    for extension in content_file_extensions:
        content_blob = f'{SETTINGS["PATH"]}/**/*{extension}'
        server.watch(content_blob, lambda: build(c))
        content_blob = f'{SETTINGS["PATH"]}/*{extension}'
        server.watch(content_blob, lambda: build(c))

    # Watch the theme's templates and static assets
    theme_path = SETTINGS["THEME"]
    server.watch(f"{theme_path}/templates/**/*.html", lambda: build(c))
    server.watch(f"{theme_path}/templates/*.html", lambda: build(c))
    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file = f"{theme_path}/static/**/*{extension}"
        server.watch(static_file, lambda: build(c))

    # Serve output path on configured port
    server.serve(port=CONFIG["port"], root=CONFIG["deploy_path"])


@task(
    help={
        "site-id": "Name of your site in Netlify.",
        "token": "Your Netlify api access token. See https://docs.netlify.com/cli/get-started/#obtain-a-token-via-the-command-line",
        "build-dir": "The folder you want to deploy",
    }
)
def deploy(c, site_id, token, build_dir):
    """Deploy to Netlify"""
    client = NetlifyClient(site_id, token)
    client.deploy(build_dir)


@task
def new_article(c, title, author="Johan Vergeer"):
    category: Optional[str] = None
    create_category: bool = False

    while category is None:
        category = input("Category: ").lower()

        if not (CONTENT_ROOT / category).exists():
            create_category = yes_or_no(
                f'Category "{category}" does not exist yet. Do you want to create it'
            )
            if create_category is False:
                category = None
                continue

    tags = [t.strip() for t in input("Tags: ").lower().split(",")]
    slug = slugify(title)

    header = f"""---
title: {title}
slug: {slug}
xref: {slug}
Tags: {",".join(tags)}
author: {author}
description: TODO
status: draft
---
"""

    filename = f"{date.today().strftime('%Y-%m-%d')}_{slug}.md"

    if create_category:
        (CONTENT_ROOT / category).mkdir()

    with open(CONTENT_ROOT / category / filename, "w") as article:
        article.write(header)
