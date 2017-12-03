import unittest

from music_player.mysql_dao import MysqlDao


class TestService(unittest.TestCase):

    def setUp(self):
        pass

    @staticmethod
    def nothing():
        pass

    def test_play_song__return_song_name(self):
        dao = MysqlDao()
        dao.get_artists()


if __name__ == '__main__':
    unittest.main()
