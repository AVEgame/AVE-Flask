from flask import Flask, render_template
from datetime import datetime
import markdown
import re

app = Flask(__name__)

with open("templates/ave.html", "r") as f:
    AVE_SPANS = f.read()

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

