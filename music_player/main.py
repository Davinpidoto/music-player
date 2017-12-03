import json

from music_player.service import Service
from music_player.artist import Artist
from music_player.config import Config
from flask import Flask, Response, send_from_directory
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
service = Service()
print("Sound Card is %s" % Config.SOUND_CARD)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('static/css', path)


@app.route('/artists')
def get_artists():
    result = service.get_artists()
    resp = Response(json.dumps(result, default=Artist.json_default))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/artists/<string:artist>')
def get_artist(artist):
    result = service.get_artist(artist)
    resp = Response(json.dumps(result, default=Artist.json_default))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/songs/<string:song>')
def play_song(song):
    return service.play_song(song)


@app.route('/albums/<string:album>')
def play_album(album):
    return service.play_album(album)


@app.route('/stop')
def stop():
    service.stop()
    return "Stopped"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
