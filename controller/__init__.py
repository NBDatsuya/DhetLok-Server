from controller.artist import artist_bp
from controller.collect import collect_bp
from controller.song import song_bp
from controller.user import user_bp


blueprint_list = [
    user_bp,
    song_bp,
    artist_bp,
    collect_bp
]
