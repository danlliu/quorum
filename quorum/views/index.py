# quorum: views/index.py

import flask
import quorum

@quorum.app.route('/')
def get_index():
    return flask.render_template('index.html')

