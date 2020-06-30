from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {
        'now': datetime.utcnow(),
        }

@app.route('/')
def index():
    return render_template("index.html", version=1.9)