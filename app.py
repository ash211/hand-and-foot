import os

from flask import Flask, flash, render_template, redirect, request, url_for
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
    form = RoundForm(request.form)
    if form.validate_on_submit():
        r = Round()
        form.populate_obj(r)
        score = r.score()
        return redirect('/?score=%d' % score)
    if request.args.get('score'):
        flash("Score: %d" % int(request.args.get('score')))
    return render_template('index.html', form=form)

@app.route('/submitRound')
def submitRound():
    form = RoundForm()

@app.route('/rules')
def rules():
    return render_template('rules.html')

if __name__ == '__main__':
    app.run(debug=True)
