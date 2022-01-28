# quorum: views/event.py

import arrow
import datetime
import flask
from flask import request, url_for
import quorum
from quorum import db

from quorum.models import Event, Response

@quorum.app.route('/event/<eventid>/')
def get_event(eventid):
    event = Event.query.filter_by(id=eventid).first_or_404()
    responses = event.responses

    going = []
    notgoing = []

    for response in responses:
        ts = arrow.get(response.updated).shift(hours=5).humanize()
        if response.attending:
            going.append({
                'name': response.name,
                'note': response.note,
                'asof': ts
            })
        else:
            notgoing.append({
                'name': response.name,
                'note': response.note,
                'asof': ts
            })

    time = arrow.get(event.time)
    timestamp = time.format(arrow.FORMAT_RSS)[:-6]
    time = time.shift(hours=5)
    timestamp += f' ({time.humanize(granularity=["day", "hour", "minute"])})'

    context = {
        'eventid': eventid,
        'name': event.name,
        'location': event.location,
        'timestamp': timestamp,
        'going': going,
        'notgoing': notgoing
    }
    return flask.render_template('event.html', **context)

@quorum.app.route('/event/', methods=['POST'])
def create_event():
    name = request.form['name']
    location = request.form['location']
    time = datetime.datetime.fromisoformat(request.form['time'])

    new_event = quorum.models.Event(name=name, location=location, time=time)
    db.session.add(new_event)
    db.session.commit()

    return flask.redirect(url_for('get_event', eventid=new_event.id))

