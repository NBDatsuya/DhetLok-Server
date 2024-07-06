import json

from model import db


class Collect(db.Model):
    __tablename__ = 'collect'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song = db.Column(db.Integer, nullable=True)
    owner = db.Column(db.Integer, nullable=True)

    def __init__(self, song=None, owner=None):
        self.song = song
        self.owner = owner

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_json(self):
        return json.dumps(self.to_dict())