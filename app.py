from datetime import datetime
import re

from flask import Flask, render_template
import markdown
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

with open("templates/ave.html", "r") as f:
    AVE_SPANS = f.read()

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