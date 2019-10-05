import os
import glob
import json
import hashlib
import markdown
from slugify import slugify
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

def load_cache():
    filelist = os.listdir(CACHE_FOLDER)
    # This one-liner does the same but I think that explicitly closing files is
    # a better practice in those cases.
    # [json.loads(open(os.path.join(CACHE_FOLDER, i), 'r').read()) for i in filelist]
    post_list = list()
    for i in filelist:
        filename = os.path.join(CACHE_FOLDER, i)
        with open(filename, 'r') as file:
            metadata = json.loads(file.read())
            post_list.append(metadata)
    return post_list

def update_posts(post_list):
    filelist = glob.glob(os.path.join(POSTS_FOLDER, '*.md'))
    filename_filter = lambda item: item['filename'] == base_file
    for i in filelist:
        with open(i, 'r') as file:
            data = file.read()
            checksum = hashlib.md5(bytes(data.encode('utf-8'))).hexdigest()
            if checksum not in [j['checksum'] for j in post_list]:
                html = md.convert(data)
                base_file = os.path.basename(i)
                try:
                    post_list.remove(next(filter(filename_filter, post_list)))
                except StopIteration:
                    pass # This means that this post isn't an update
                post = md.Meta
                post['filename'] = base_file
                post['slug'] = slugify(post['title'][0])
                post['checksum'] = checksum
                post['content'] = html
                save_to_cache(post)
                post_list.append(post)
    return post_list

def get_posts_list(update=False):
    posts = load_cache()
    if update:
        posts = update_posts(posts)
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
