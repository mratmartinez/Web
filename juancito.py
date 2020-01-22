import os
import re
import csv
import glob
import json
import string
import locale
import hashlib
import markdown
import configparser
from datetime import datetime

import unidecode
from flask import Flask, render_template
from flask_cache import Cache

from utils import logger

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Is this debug?
DEBUG = config.getboolean('DEFAULT', 'Debug')
if DEBUG is True:
    logger.setLevel(10)
else:
    logger.setLevel(20)

# Working locale
LOCALE = config['DEFAULT']['Locale']
logger.info(LOCALE)
locale.setlocale(locale.LC_TIME, LOCALE)


csv_parse = csv.reader([config['DEFAULT']['MarkdownExtensions']])
MARKDOWN_EXTENSIONS = [i.strip() for i in list(csv_parse)[0]]
logger.info(MARKDOWN_EXTENSIONS)
del(csv_parse)

md = markdown.Markdown(extensions=['meta']+MARKDOWN_EXTENSIONS,
                       # Because of a bug
                       extension_configs={'footnotes': {'BACKLINK_TEXT': ''}})

SITE_NAME = config['DEFAULT']['SiteName']
POSTS_FOLDER = config['FILESYSTEM']['PostsFolder']
CACHE_FOLDER = config['FILESYSTEM']['CacheFolder']
STATIC_FOLDER = config['FILESYSTEM']['StaticFolder']
ABOUT_FILE = config['FILESYSTEM']['AboutFile']


def slugify(text):
    """
    Returns a slug string valid for URLs.
    """
    ascii_text = unidecode.unidecode(text)
    return re.sub(r'[-\s]+', '-',
                  (re.sub(r'[^\w\s-]', '', ascii_text).strip().lower()))


# def get_cache_files(folder):
#     """
#     List the files in a folder. If the folder doesn't exists, it creates it.
#     """
#     try:
#         files = os.listdir(folder)
#     except FileNotFoundError:
#         os.mkdir(folder)
#         files = list()
#     logger.debug(files)
#     return files


# def load_cache():
#     """
#     Read the posts in CACHE_FOLDER and returns a list with the results.
#     """
#     cachefiles = get_cache_files(CACHE_FOLDER)
#     filelist = [os.path.join(CACHE_FOLDER, i) for i in cachefiles]
#     postlist = [json.loads(open(cache, 'r').read()) for cache in filelist]
#     return postlist


# def get_file_data(filename):
#     """
#     Read the contents of a post's file and return it along with its MD5 hash.
#     """
#     with open(filename, 'r') as opened:
#         data = opened.read()
#         checksum = hashlib.md5(bytes(data.encode('utf-8'))).hexdigest()
#     return data, checksum


def format_date(datestring):
    """
    Returns a properly formatted date according to the language used.
    """
    logger.debug(datestring)
    day = datetime.strptime(datestring, "%Y-%m-%d")
    if locale.getlocale(locale.LC_TIME)[0] == "es_AR":
        # In case we are displaying the web in spanish.
        formatted_day = day.strftime("%A %d de %B de %Y")
        capitalized_day = string.capwords(formatted_day, " de ")
    else:
        capitalized_day = day.strftime("%c")
    return capitalized_day


# def update_md(basefile, data, checksum):
#     """
#     Reads a Markdown file and returns a dict with metadata.
#     """
#     html = md.convert(data)
#     post = md.Meta
#     post['filename'] = basefile
#     post['slug'] = slugify(post['title'][0])
#     post['checksum'] = checksum
#     post['date'] = post['date'][0]
#     post['form_date'] = format_date(post['date'])
#     post['content'] = html
#     return post


def format_post(data):
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


# def save_to_cache(post_dict):
#     """
#     Saves the recently updated Markdown in the cache as a JSON file.
#     """
#     meta = json.dumps(post_dict)
#     postname = post_dict['filename'][0:-3]
#     filename = os.path.join(CACHE_FOLDER, postname) + '.json'
#     with open(filename, 'w') as cache:
#         cache.write(meta)


# def check_new_posts(postlist):
#     """
#     Checks if there are new posts or updates to the old ones.
#     In any case, it returns a new list with all the posts, updated or not.
#     """
#     filelist = glob.glob(os.path.join(POSTS_FOLDER, '*.md'))
#     def filename_filter(item): item['filename'] == basefile
#     for i in filelist:
#         data, checksum = get_file_data(i)
#         if checksum not in [j['checksum'] for j in postlist]:
#             basefile = os.path.basename(i)
#             post = update_md(basefile, data, checksum)
#             try:
#                 postlist.remove(next(filter(filename_filter, postlist)))
#             except StopIteration:
#                 pass  # This means that this post isn't an update
#             save_to_cache(post)
#             postlist.append(post)
#     return postlist


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


# def sort_posts_by_date(postlist):
#     """
#     This is a bugfix. Self-explained.
#     """
#     def post_filter(item): return datetime.strptime(item['date'], "%Y-%m-%d")
#     postlist = sorted(postlist, key=post_filter)
#     logger.debug([post['date'] for post in postlist])
#     return postlist


# def get_posts_list(update=True):
#     """
#     This is the old version of this function.
#     """
#     posts = load_cache()
#     if update:
#         posts = check_new_posts(posts)
#     postlist = sort_posts_by_date(posts)
#     return postlist


@cache.memoize(timeout=50)
def get_post_from_slug(slug):
    """
    Receives an slug string and returns the matching post.
    """
    posts = get_postlist()
    post = next(filter(lambda item: item['slug'] == slug, posts))
    logger.debug((type(post), id(post)))
    return post


@cache.memoize(timeout=50)
def get_postlist():
    """
    Loads only the cached posts, unless the 'update' flag is True.
    In that case, it will check for new posts, even if no changes were made.
    Merged with sort_posts_by_date()
    """
    postlist = read_posts()
    def post_filter(item): return datetime.strptime(item['date'], "%Y-%m-%d")
    postlist = sorted(postlist, key=post_filter)
    logger.debug([post['date'] for post in postlist])
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
        data = file.read()
        content = md.convert(data)
    return render_template("about.html", content=content)
