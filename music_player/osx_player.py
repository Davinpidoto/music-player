import subprocess

from music_player.config import Config


class OsxPlayer:

    @staticmethod
    def stop():
        print("stop")
        command = "killall afplay"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    @staticmethod
    def play_song(song):
        song_with_path = "%s/%s" % (Config.SOURCE_ROOT, song)
        print(song_with_path)
        subprocess.Popen(['afplay', song_with_path], stdout=subprocess.PIPE)

    @staticmethod
    def play_song_blocking(song):
        song_with_path = "%s/%s" % (Config.SOURCE_ROOT, song)
        subprocess.call(['afplay', song_with_path])
