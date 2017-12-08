import subprocess
from music_player.config import Config


class OsxPlayer:

    @staticmethod
    def stop():
        subprocess.Popen(['killall', 'afplay'], stdout=subprocess.PIPE)

    @staticmethod
    def play_song_blocking(song):
        print(song)
        song_with_path = "%s/%s" % (Config.SOURCE_ROOT, song)
        subprocess.call(['afplay', song_with_path])
