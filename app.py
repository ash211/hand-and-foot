import os

from flask import Flask, flash, jsonify, render_template, redirect, request, url_for
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from score import scoreState

app = Flask(__name__)
app.secret_key = 's3cr3t'
Heroku(app)
Bootstrap(app)
db = SQLAlchemy(app)

from models import *

@app.route('/', methods=('GET', 'POST'))
def main():
    return render_template('index.html', form=RoundForm())

@app.route('/submitRound', methods=('POST', ))
def submitRound():
    form = RoundForm(request.form)
    #print("request.form: ", request.form)
    #print("form.data", form.data)
    form.validate()
    #print("errors: ", form.errors)
    if form.validate_on_submit():
        #print('Form was valid')
        r = Round()
        form.populate_obj(r)
        try:
            score = r.score()
            return jsonify({"score": score})
        except Exception as e:
            return "Invalid: %s" % e
    else:
        return "invalid"

@app.route('/rules')
def rules():
    return render_template('rules.html')

if __name__ == '__main__':
    app.run(debug=True)
