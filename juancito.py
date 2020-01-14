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

from utils import logger

app = Flask(__name__)
config = configparser.ConfigParser()
CONFIG_FILE = 'config.ini'
config.read(CONFIG_FILE)


# Is this debug?
DEBUG = config.getboolean('DEFAULT','Debug')
if DEBUG == True:
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
    """Returns a slug string valid for URLs."""
    ascii_text = unidecode.unidecode(text)
    return re.sub(r'[-\s]+', '-',
                  (re.sub(r'[^\w\s-]', '', ascii_text).strip().lower()))


def get_cache_files(folder):
    """List the files in a folder. If the folder doesn't exists, it creates it."""
    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        os.mkdir(folder)
        files = list()
    logger.debug(files)
    return files


def load_cache():
    """Read the posts in CACHE_FOLDER and returns a list with the results."""
    filelist = [os.path.join(CACHE_FOLDER, i) for i in get_cache_files(CACHE_FOLDER)]
    postlist = [json.loads(open(cache, 'r').read()) for cache in filelist]
    return postlist


def get_file_data(filename):
    """Read the contents of a post's file and return it along with its MD5 hash."""
    with open(filename, 'r') as opened:
        data = opened.read()
        checksum = hashlib.md5(bytes(data.encode('utf-8'))).hexdigest()
    return data, checksum


def format_date(datestring):
    """Returns a properly formatted date according to the language used."""
    day = datetime.strptime(datestring, "%Y-%m-%d")
    if locale.getlocale(locale.LC_TIME)[0] == "es_AR":
        # In case we are displaying the web in spanish.
        formatted_day = day.strftime("%A %d de %B de %Y")
        capitalized_day = string.capwords(formatted_day, " de ")
    else:
        capitalized_day = day.strftime("%c")
    return capitalized_day


def update_md(basefile, data, checksum):
    """Reads a Markdown file and returns a dict with metadata."""
    html = md.convert(data)
    post = md.Meta
    post['filename'] = basefile
    post['slug'] = slugify(post['title'][0])
    post['checksum'] = checksum
    post['date'] = format_date(post['date'][0])
    post['content'] = html
    return post


def save_to_cache(post_dict):
    """Saves the recently updated Markdown in the cache as a JSON file."""
    meta = json.dumps(post_dict)
    filename = os.path.join(CACHE_FOLDER, post_dict['filename'][0:-3]) + '.json'
    with open(filename, 'w') as cache:
        cache.write(meta)


def check_new_posts(postlist):
    """
    Checks if there are new posts or updates to the old ones.
    In any case, it returns a new list with all the posts, updated or not.
    """
    filelist = glob.glob(os.path.join(POSTS_FOLDER, '*.md'))
    filename_filter = lambda item: item['filename'] == basefile  # noqa
    for i in filelist:
        data, checksum = get_file_data(i)
        if checksum not in [j['checksum'] for j in postlist]:
            basefile = os.path.basename(i)
            post = update_md(basefile, data, checksum)
            try:
                postlist.remove(next(filter(filename_filter, postlist)))
            except StopIteration:
                pass  # This means that this post isn't an update
            save_to_cache(post)
            postlist.append(post)
    return postlist


def get_posts_list(update=False):
    """
    Loads only the cached posts, unless the 'update' flag is True.
    In that case, it will check for new posts, even if no changes were made.
    """
    posts = load_cache()
    if update:
        posts = check_new_posts(posts)
    return posts


def get_post_from_slug(slug):
    """Receives an slug string and returns the matching post."""
    slug_filter = lambda item: item['slug'] == slug  # noqa
    posts = get_posts_list()
    post = next(filter(slug_filter, posts))
    return post


@app.route('/')
def index():
    posts = get_posts_list(True)
    return render_template("index.html", blog_list=reversed(posts))


@app.route('/post/<slug>')
def post(slug):
    post = get_post_from_slug(slug)
    return render_template("post.html", post=post)


@app.route('/about')
def about():
    with open(ABOUT_FILE, 'r') as file:
        data = file.read()
        content = md.convert(data)
    return render_template("about.html", content=content)
