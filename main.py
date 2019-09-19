from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the test'

@app.route('/about')
def about():
    return 'This is my about page'
