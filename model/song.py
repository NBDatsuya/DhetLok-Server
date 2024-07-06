from model import db


class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    real_name = db.Column(db.String(100), nullable=True)
    artist = db.Column(db.String(100), nullable=True)
    file_url = db.Column(db.String(100), nullable=True)
    hits = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.Integer, nullable=True)

    def __init__(self, real_name=None, artist=None, file_url=None, hits=None, genre=None):
        self.real_name = real_name
        self.artist = artist
        self.file_url = file_url
        self.hits = hits
        self.genre = genre
