import subprocess

from music_player.config import Config


class LinuxPlayer:

    @staticmethod
    def stop():
        subprocess.Popen(['killall', 'aplay'], stdout=subprocess.PIPE)

    @staticmethod
    def play_song_blocking(song):
        song_with_path = "%s/%s" % (Config.SOURCE_ROOT, song)
        print(song)
        subprocess.call(['aplay', '-Ddefault:CARD=%s' % Config.SOUND_CARD, song_with_path])
