import os
import csv
import glob
import locale
import configparser
from datetime import datetime

import markdown
from flask import Flask, render_template
from flask_caching import Cache
from babel.dates import format_date

from utils import slugify
from utils import logger as LOGGER

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

csv_parse = csv.reader([config['DEFAULT']['MarkdownExtensions']])
MARKDOWN_EXTENSIONS = [i.strip() for i in list(csv_parse)[0]]
LOGGER.info(MARKDOWN_EXTENSIONS)
del(csv_parse)

SITE_NAME = config['DEFAULT']['SiteName']
POSTS_FOLDER = config['FILESYSTEM']['PostsFolder']
CACHE_FOLDER = config['FILESYSTEM']['CacheFolder']
STATIC_FOLDER = config['FILESYSTEM']['StaticFolder']
ABOUT_FILE = config['FILESYSTEM']['AboutFile']


def format_post(data):
    """
    Receives a post metadata and format it properly in order to use it.
    """
    get_only = lambda var, key: var[key][0]
    md = markdown.Markdown(extensions=['meta'] + MARKDOWN_EXTENSIONS)
    html = md.convert(data)
    post = md.Meta
    for key in ['category', 'author', 'title', 'date', 'language', 'summary']:
        post[key] = get_only(post, key)
        LOGGER.debug(post[key])
    post['slug'] = slugify(post['title'])
    if post['language'] == "ES":
        locale = "es_AR.UTF-8"
    else:
        locale = "en_GB.UTF-8"
    date = datetime.strptime(post['date'], "%Y-%m-%d")
    post['form_date'] = format_date(date=date,
                                    format="full",
                                    locale=locale)
    post['content'] = html
    return post


def read_posts():
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
def get_post_from_slug(slug):
    """
    Receives an slug string and returns the matching post.
    """
    posts = get_postlist()
    post = next(filter(lambda item: item['slug'] == slug, posts))
    LOGGER.debug((type(post), id(post)))
    return post


@cache.memoize(timeout=50)
def get_postlist():
    """
    Loads only the cached posts, unless the 'update' flag is True.
    In that case, it will check for new posts, even if no changes were made.
    Merged with sort_posts_by_date()
    """
    postlist = read_posts()

    def post_filter(item):
        return datetime.strptime(item['date'], "%Y-%m-%d")

    postlist = sorted(postlist, key=post_filter)
    LOGGER.debug([post['date'] for post in postlist])
    return postlist


@cache.cached(timeout=50)
@app.route('/')
def index():
    posts = get_postlist()
    return render_template("index.html", blog_list=reversed(posts))


@cache.cached(timeout=50)
@app.route('/post/<slug>')
def post(slug):
    post = get_post_from_slug(slug)
    return render_template("post.html", post=post)


@cache.cached(timeout=50)
@app.route('/about')
def about():
    with open(ABOUT_FILE, 'r') as file:
        md = markdown.Markdown(extensions=['meta'] + MARKDOWN_EXTENSIONS)
        data = file.read()
        content = md.convert(data)
    return render_template("about.html", content=content)


