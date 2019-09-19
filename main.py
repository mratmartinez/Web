import glob
import os
from markdown import markdown
from flask import Flask, render_template

DEBUG = True
POSTS_FOLDER = "posts"
SITE_NAME = 'La web de Juancito'

app = Flask(__name__)

def get_posts():
    filelist = glob.glob(os.path.join(POSTS_FOLDER, '*.md'))
    posts = list()
    for i in filelist:
        with open(i, 'r') as file:
            posts.append(markdown(file.read(), extensions=['fenced_code']))
    return posts

@app.route('/')
def index():
    posts = get_posts()
    return render_template("index.html", blog_list=posts)

@app.route('/about')
def about():
    return 'This is my about page'
