import subprocess

from music_player.config import Config


class LinuxPlayer:

    @staticmethod
    def stop():
        command = "killall aplay"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    @staticmethod
    def play_song(song):
        song_with_path = "%s/%s" % (Config.SOURCE_ROOT, song)
        subprocess.Popen(['aplay', '-Ddefault:CARD=%s' % Config.SOUND_CARD, song_with_path], stdout=subprocess.PIPE)

    @staticmethod
    def play_song_blocking(song):
        song_with_path = "%s/%s" % (Config.SOURCE_ROOT, song)
        subprocess.call(['aplay', '-Ddefault:CARD=%s' % Config.SOUND_CARD, song_with_path])
