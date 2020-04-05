import os
import re
import csv
import glob
import json
import string
import locale
import hashlib
import configparser
from datetime import datetime

import markdown
import unidecode
from flask import Flask, render_template
from flask_caching import Cache

from utils import logger as LOGGER
from utils import slugify

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Is this debug?
DEBUG = config.getboolean('DEFAULT', 'Debug')
if DEBUG is True:
    LOGGER.setLevel(10)
else:
    LOGGER.setLevel(20)

# Working locale
LOCALE = config['DEFAULT']['Locale']
LOGGER.info(LOCALE)
locale.setlocale(locale.LC_TIME, LOCALE)


csv_parse = csv.reader([config['DEFAULT']['MarkdownExtensions']])
MARKDOWN_EXTENSIONS = [i.strip() for i in list(csv_parse)[0]]
LOGGER.info(MARKDOWN_EXTENSIONS)
del(csv_parse)

md = markdown.Markdown(extensions=['meta']+MARKDOWN_EXTENSIONS,
                       # Because of a bug
                       extension_configs={'footnotes': {'BACKLINK_TEXT': ''}})

SITE_NAME = config['DEFAULT']['SiteName']
POSTS_FOLDER = config['FILESYSTEM']['PostsFolder']
CACHE_FOLDER = config['FILESYSTEM']['CacheFolder']
STATIC_FOLDER = config['FILESYSTEM']['StaticFolder']
ABOUT_FILE = config['FILESYSTEM']['AboutFile']


class Juancito:
    def format_date(self, datestring):
        """
        Returns a properly formatted date according to the language used.
        """
        LOGGER.debug(datestring)
        day = datetime.strptime(datestring, "%Y-%m-%d")
        if locale.getlocale(locale.LC_TIME)[0] == "es_AR":
            # In case we are displaying the web in spanish.
            formatted_day = day.strftime("%A %d de %B de %Y")
            capitalized_day = string.capwords(formatted_day, " de ")
        else:
            capitalized_day = day.strftime("%c")
        return capitalized_day


    def format_post(self, data):
        """
        Receives a post metadata and format it properly in order to use it.
        """
        html = md.convert(data)
        post = md.Meta
        post['slug'] = slugify(post['title'][0])
        post['date'] = post['date'][0]
        post['form_date'] = format_date(post['date'])
        post['content'] = html
        return post


    def read_posts(self):
        """
        Reads the .md files and converts it to Markdown.
        """
        postlist = list()
        filelist = glob.glob(os.path.join(POSTS_FOLDER, '*.md'))
        for i in filelist:
            with open(i, 'r') as opened:
                data = opened.read()
                post = format_post(data)
                postlist.append(post)
        return postlist


    @cache.memoize(timeout=50)
    def get_post_from_slug(self, slug):
        """
        Receives an slug string and returns the matching post.
        """
        posts = get_postlist()
        post = next(filter(lambda item: item['slug'] == slug, posts))
        LOGGER.debug((type(post), id(post)))
        return post


    @cache.memoize(timeout=50)
    def get_postlist(self):
        """
        Loads only the cached posts, unless the 'update' flag is True.
        In that case, it will check for new posts, even if no changes were made.
        Merged with sort_posts_by_date()
        """
        postlist = read_posts()
        def post_filter(item): return datetime.strptime(item['date'], "%Y-%m-%d")
        postlist = sorted(postlist, key=post_filter)
        LOGGER.debug([post['date'] for post in postlist])
        return postlist


    @cache.cached(timeout=50)
    @app.route('/')
    def index(self):
        posts = get_postlist()
        return render_template("index.html", blog_list=reversed(posts))


    @cache.cached(timeout=50)
    @app.route('/post/<slug>')
    def post(self, slug):
        post = get_post_from_slug(slug)
        return render_template("post.html", post=post)


    @cache.cached(timeout=50)
    @app.route('/about')
    def about(self):
        with open(ABOUT_FILE, 'r') as file:
            data = file.read()
            content = md.convert(data)
        return render_template("about.html", content=content)
