from datetime import datetime
import re
import json
import collections

from flask import Flask, render_template, jsonify, request
import markdown
from werkzeug.exceptions import HTTPException
from ave import Game, Character
from ave import AVE, config, load_game_from_file
from ave.exceptions import AVEGameOver, AVEWinner

app = Flask(__name__)

with open("templates/ave.html", "r") as f:
    AVE_SPANS = f.read()

def get_game_list():
    with open("gamelist.json", "r") as f:
        d = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(f.read())
    return d

def get_room_info(filename, data):
    numbers = data["numbers"]
    inventory = data["inventory"]
    current_room = data["current_room"]
    option_key = data["option"]
    character = Character(numbers=numbers, inventory=inventory)
    game = load_game_from_file(filename)
    game.load()
    if option_key is None:
        game.reset()
        character.reset(game.items)
    else:
        option_key = int(option_key)
        game.id = current_room
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
    return {
        "room": game.id,
        "room_desc": text,
        "options": options_list,
        "inventory": character.inventory,
        "numbers": character.numbers,
        "inventory_text": inventory_text,
    }

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

@app.route('/play/<filename>', methods=['GET', 'POST'])
def play(filename):
    if request.method == 'GET':
        return render_template('play.html', filename=filename)
    elif request.method == 'POST':
        data = request.json
        print(data)
        room_info = get_room_info(filename, data)
        return jsonify(room_info)

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
