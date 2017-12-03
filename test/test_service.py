import unittest
from unittest.mock import patch

from music_player import Service


class TestService(unittest.TestCase):

    def setUp(self):
        pass

    @staticmethod
    def nothing():
        pass

    @patch('music_player.service.Dao.get_song')
    @patch.multiple('music_player.service.Player', play_song=nothing, stop=nothing)
    def play_song__return_song_name(self, get_song):
        get_song.return_value = 'song1.wav'
        service = Service()
        song = service.play_song("1")
        assert song == "song1.wav"


if __name__ == '__main__':
    unittest.main()
