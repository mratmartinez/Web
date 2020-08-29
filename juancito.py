import os
import csv
import glob
import configparser

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

md = markdown.Markdown(
    extensions=['meta'] + MARKDOWN_EXTENSIONS,
    # Because of a bug
    extension_configs={'footnotes': {
        'BACKLINK_TEXT': ''
    }})

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

    def post_filter(item):
        return datetime.strptime(item['date'], "%Y-%m-%d")

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

