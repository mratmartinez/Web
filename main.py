import os
import glob
import json
import hashlib
import markdown
from slugify import slugify
from flask import Flask, render_template

SITE_NAME = 'La web de Juancito'
DEBUG = True
POSTS_FOLDER = 'posts'
CACHE_FOLDER = 'cache'
# For some reason, Markdown module's "meta" extension creates a list for
# every value so we need to call them with index=0
LIST_TAGS = ['title', 'date', 'summary']
# Now that I added this declaration, it's a great moment to explain that the
# date tag *must* be formated following the ISO 8601

app = Flask(__name__)
md = markdown.Markdown(extensions=['fenced_code', 'meta'])

def get_posts():
    filelist = glob.glob(os.path.join(POSTS_FOLDER, '*.md'))
    posts = list()
    for i in filelist:
        with open(i, 'r') as file:
            data = file.read()
            checksum = hashlib.md5(bytes(data.encode("utf-8"))).hexdigest()
            html = md.convert(data)
            post = md.Meta
            post['checksum'] = checksum
            post['content'] = html
            # Those values are outside of a list, unlike the ones generated
            # automatically. So we'll iterate over the rest of the tags in
            # order to make some consistence adjustments.
            for tag in LIST_TAGS:
                post[tag] = post[tag][0]
            post_to_cache(post)
            posts.append(post)
    return posts

def post_to_cache(post_dict):
    meta = json.dumps(post_dict)
    slug = post_dict['date'] + '-' + slugify(post_dict['title'])
    filename = os.path.join(CACHE_FOLDER, slug) + '.json'
    with open(filename, 'w') as cache:
        cache.write(meta)

@app.route('/')
def index():
    posts = get_posts()
    return render_template("index.html", blog_list=posts)

@app.route('/about')
def about():
    return 'This is my about page'
