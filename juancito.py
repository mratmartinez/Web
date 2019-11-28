import os
import re
import glob
import json
import string
import locale
import hashlib
import markdown
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
md = markdown.Markdown(extensions=['fenced_code',
                                   'meta',
                                   'abbr',
                                   'footnotes'],
                      extension_configs={
                          'footnotes': {
                              'BACKLINK_TEXT': ''}}) # This is because of a bug

SITE_NAME = 'La web de Juancito'
DEBUG = True
POSTS_FOLDER = 'posts'
CACHE_FOLDER = 'cache'
STATIC_FOLDER = 'static'
ABOUT_FILE = os.path.join(STATIC_FOLDER, 'about.md')
locale.setlocale(locale.LC_TIME, "es_AR")

def slugify(string):
    return re.sub(r'[-\s]+', '-',
            (re.sub(r'[^\w\s-]', '',string).strip().lower()))

def get_cache_files(folder):
    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        os.mkdir(folder)
        files = list()
    return files

def load_cache():
    filelist = [os.path.join(CACHE_FOLDER, i) for i in get_cache_files(CACHE_FOLDER)]
    postlist = [json.loads(open(cache, 'r').read()) for cache in filelist]
    return postlist

def get_file_data(filename):
    with open(filename, 'r') as opened:
        data = opened.read()
        checksum = hashlib.md5(bytes(data.encode('utf-8'))).hexdigest()
    return data, checksum

def format_date(datestring):
    day = datetime.strptime(datestring, "%Y-%m-%d")
    if locale.getlocale(locale.LC_TIME)[0] == "es_AR":
        formatted_day = day.strftime("%A %w de %B de %Y")
        capitalized_day = string.capwords(formatted_day, " de ")
    else:
        capitalized_day = day.strftime("%c")
    return capitalized_day

def update_md(basefile, data, checksum):
    html = md.convert(data)
    post = md.Meta
    post['filename'] = basefile
    post['slug'] = slugify(post['title'][0])
    post['checksum'] = checksum
    post['date'] = format_date(post['date'][0])
    post['content'] = html
    return post

def check_new_posts(postlist):
    filelist = glob.glob(os.path.join(POSTS_FOLDER, '*.md'))
    filename_filter = lambda item: item['filename'] == basefile
    for i in filelist:
        data, checksum = get_file_data(i)
        if checksum not in [j['checksum'] for j in postlist]:
            basefile = os.path.basename(i)
            post = update_md(basefile, data, checksum)
            try:
                postlist.remove(next(filter(filename_filter, postlist)))
            except StopIteration:
                pass # This means that this post isn't an update
            save_to_cache(post)
            postlist.append(post)
    return postlist

def get_posts_list(update=False):
    posts = load_cache()
    if update:
        posts = check_new_posts(posts)
    return posts

def get_post_from_slug(slug):
    slug_filter = lambda item: item['slug'] == slug
    posts = get_posts_list()
    post = next(filter(slug_filter, posts))
    return post

def save_to_cache(post_dict):
    meta = json.dumps(post_dict)
    filename = os.path.join(CACHE_FOLDER, post_dict['filename'][0:-3]) + '.json'
    with open(filename, 'w') as cache:
        cache.write(meta)

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
