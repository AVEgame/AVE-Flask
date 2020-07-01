from datetime import datetime
import re
import json
import collections

from flask import Flask, render_template, jsonify
import markdown
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

with open("templates/ave.html", "r") as f:
    AVE_SPANS = f.read()

def get_game_list():
    with open("gamelist.json", "r") as f:
        d = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(f.read())
    return d

@app.errorhandler(HTTPException)
def error(e):
    return render_template("error.html", code=e.code)

@app.context_processor
def inject():
    return {
        'now': datetime.utcnow(),
        'version': 1.9,
        }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/docs/<filename>')
def docs(filename):
    with open(f"AVE-docs/docs/{filename}", "r") as f:
        text = f.read()
    html = markdown.markdown(text, extensions=['tables', 'fenced_code']).replace(" AVE ", f" {AVE_SPANS} ")
    html = re.sub(r"\%\%([^\%]*)\%\%", r'<span style="color:#4d9906"><<i>\1</i>></span>', html)
    return render_template("docs.html", content=html)

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/make')
def make():
    return render_template('make.html')

@app.route('/git')
def git():
    return render_template('git.html')

@app.route('/play/<filename>')
def play(filename):
    return render_template('play.html', filename=filename)

@app.route('/play')
def select():
    return render_template('select.html', user=False)

@app.route('/play/user')
def user_play():
    return render_template('select.html', user=True)

@app.route('/gamelist.json')
def gamelist():
    d = get_game_list()
    return jsonify(d)

@app.route('/library')
def lib():
    d = get_game_list()
    return render_template('library.html', game_list=d)
