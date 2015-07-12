import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

if __name__ == '__main__':
    app.run(debug=True)
