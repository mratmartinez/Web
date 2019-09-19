from flask import Flask, render_template
app = Flask(__name__)

TEMPLATES_FOLDER = 'templates'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return 'This is my about page'
