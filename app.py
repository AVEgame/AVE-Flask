from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {
        'now': datetime.utcnow(),
        'ave': "<span style='color:#CC0000'>A</span><span style='color:#4d9906'>V</span><span style='color:#32619e'>E</span>",
        }

@app.route('/')
def index():
    return render_template("index.html", version=1.9)