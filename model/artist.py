from model import db


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    real_name = db.Column(db.String(64), nullable=True)
    genre = db.Column(db.Integer, nullable=True)
    img_url = db.Column(db.Text, nullable=True)
    hot = db.Column(db.Boolean, nullable=True)

    def __init__(self, real_name=None, genre=None, img_url=None, hot=None):
        self.real_name = real_name
        self.genre = genre
        self.img_url = img_url
        self.hot = hot
