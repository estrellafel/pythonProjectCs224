"""
Main python file for our flask project

@author: Felix Estrella
"""

from distutils.log import error
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', error = error)

if __name__ == "__main__":
    app.run()


