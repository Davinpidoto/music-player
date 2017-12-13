import logging
import sys


class Config:

    LAVRY = "DA"
    INTERNAL = "ALSA"
    MYSQL_URL = 'mysql+mysqlconnector://pi:pi@localhost:3306/music'

    if sys.platform == "darwin":
        SOURCE_ROOT = "/Users/davin/Music/iTunes/iTunes Media/Music"
        SOUND_CARD = INTERNAL
    else:
        SOURCE_ROOT = "/media/hd/music"
        SOUND_CARD = LAVRY

    LOG = "mp.log"
    logging.basicConfig(filename=LOG, level=logging.INFO)
    log = logging.getLogger(__name__)

    def __init__(self):
        pass
