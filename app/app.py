from datetime import datetime
import re
import json
import collections
import os

from flask import Flask, render_template, jsonify, request, make_response
import markdown
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from ave import Game, Character, load_game_from_file
from ave import config as aveconfig
from ave.exceptions import AVEGameOver, AVEWinner
import magic

from git_handler import GitManager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

with open("config.json", "r") as f:
    CONFIG = json.load(f)

GIT_KEY = CONFIG["git_key"]

with open("templates/ave.html", "r") as f:
    AVE_SPANS = f.read()

def get_game_list():
    with open(os.path.join(aveconfig.root_folder, "gamelist.json"), "r") as f:
        games = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(f.read())
    for game in games:
        game["user"] = False
    if "user_games_dir" in CONFIG:
        user_dir = CONFIG["user_games_dir"]
        with open(os.path.join(user_dir, "gamelist.json"), "r") as f:
            user_games = json.load(f)
            for game in user_games:
                game["user"] = True
            games += user_games
    return games

def get_room_info(filename, data, user=False):
    numbers = data["numbers"]
    inventory = data["inventory"]
    current_room = data["current_room"]
    option_key = data["option"]
    if user:
        path = os.path.join(CONFIG["user_games_dir"], filename)
    else:
        path = os.path.join(aveconfig.games_folder, filename)
    game = load_game_from_file(path)
    game.load()
    if option_key is None:
        character = Character()
        character.reset(game.items)
    else:
        option_key = int(option_key)
        character = Character(numbers=numbers, inventory=inventory, location=current_room)
        game.pick_option(option_key, character)
    try:
        text, options = game.get_room_info(character)
    except AVEGameOver:
        return {"room": "__GAMEOVER__"}
    except AVEWinner:
        return {"room": "__WINNER__"}
    options_list = []
    for k, v in options.items():
        options_list.append((k, v))
    options_list = sorted(options_list, key=lambda x: x[0])
    inventory_text = character.get_inventory(game.items)
    data = {
        "room": character.location,
        "room_desc": text,
        "options": options_list,
        "inventory": character.inventory,
        "numbers": character.numbers,
        "inventory_text": inventory_text,
    }
    return data

@app.errorhandler(HTTPException)
def error(e):
    message = ""
    if e.code == 413:
        message = "File size too large, please try again"
    return render_template("error.html", code=e.code, message=message)

@app.context_processor
def inject():
    return {
        'now': datetime.utcnow(),
        'version': aveconfig.version.strip(),
        }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/docs/<filename>')
def docs(filename):
    with open(f"AVE-docs/{filename}", "r") as f:
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

@app.route('/play/<filename>', methods=['GET', 'POST'])
@app.route('/play/user/<filename>', methods=['GET', 'POST'])
def play(filename):
    user = False
    request_path = request.path.split("/")
    if len(request_path) == 4 and request_path[2] == "user":
        user = True
    if request.method == 'GET':
        if user:
            filename = 'user/' + filename
        return render_template('play.html', filename=filename)
    elif request.method == 'POST':
        data = request.json
        try:
            room_info = get_room_info(filename, data, user=user)
            return jsonify(room_info)
        except:
            return render_template("play_error.html", data=data), 500

@app.route('/download/<filename>')
@app.route('/download/user/<filename>')
def download(filename):
    user = False
    request_path = request.path.split("/")
    if len(request_path) == 4 and request_path[2] == "user":
        user = True
    if user:
        path = os.path.join(CONFIG['user_games_dir'], filename)
    else:
        path = os.path.join(aveconfig.games_folder, filename)
    with open(path, "r") as f:
        response =  make_response(f.read(), 200)
        response.mimetype = "text/plain"
        return response

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
@app.route('/library/debug')
def lib():
    debug = "debug" in request.path
    d = get_game_list()
    return render_template('library.html', game_list=d, debug=debug)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        no_file = False
        if 'avefile' not in request.files:
            no_file = True
        file = request.files['avefile']
        filename = file.filename
        if not filename or no_file:
            error = "No file uploaded"
            return render_template('add.html', error=error)
        if filename.split(".")[-1] != "ave":
            error = "File must have .ave as it's extension"
            return render_template('add.html', error=error)
        filename = secure_filename(filename)
        content = file.read()
        if 'ascii text' not in magic.from_buffer(content).lower():
            error = "File contents not supported. File must contain ASCII text"
            return render_template('add.html', error=error)
        git = GitManager(GIT_KEY)
        try:
            link = git.add_file(filename, content)
        except:
            error = """
            There was an error communicating with the GitHub API.
            Please try again later.
            """
            return render_template('add.html', error=error)
        return render_template('success.html', link=link)
