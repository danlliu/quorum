# quorum: views/response.py

import datetime
import flask
from flask import request, url_for
import time
import quorum
from quorum import db

from quorum.models import Event, Response

@quorum.app.route('/event/<eventid>/response/', methods=['POST'])
def create_response(eventid):
    name = request.form['name']
    attending = 'attending' in request.form
    note = request.form['note']
    timestamp = datetime.datetime.fromtimestamp(time.time())

    event = Event.query.filter_by(id=eventid).first_or_404()
    if any(r.name == name for r in event.responses):
        resp = None
        for r in event.responses:
            if r.name == name:
                resp = r
                break
        resp.attending = attending
        resp.note = note
        resp.updated = timestamp
        db.session.commit()
    else:
        resp = Response(eventid=eventid, name=name, attending=attending, note=note, updated=timestamp)
        db.session.add(resp)
        db.session.commit()

    return flask.redirect(url_for('get_event', eventid=eventid))
