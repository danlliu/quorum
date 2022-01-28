# quorum: models.py

import uuid
from quorum import db
from sqlalchemy.dialects.postgresql import UUID

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String())
    location = db.Column(db.String())
    time = db.Column(db.DateTime())
    responses = db.relationship('Response', backref='event', lazy=True)

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    eventid = db.Column(UUID(as_uuid=True), db.ForeignKey('events.id'), nullable=False)
    name = db.Column(db.String())
    attending = db.Column(db.Boolean)
    note = db.Column(db.String())
    updated = db.Column(db.DateTime())

