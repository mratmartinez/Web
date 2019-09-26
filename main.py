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

app = Flask(__name__)
md = markdown.Markdown(extensions=['fenced_code', 'meta'])

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

def get_posts(post_list):
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

def save_to_cache(post_dict):
    meta = json.dumps(post_dict)
    filename = os.path.join(CACHE_FOLDER, post_dict['filename'][0:-3]) + '.json'
    with open(filename, 'w') as cache:
        cache.write(meta)

@app.route('/')
def index():
    posts = load_cache()
    posts = get_posts(posts)
    return render_template("index.html", blog_list=posts)

@app.route('/about')
def about():
    return 'This is my about page'
