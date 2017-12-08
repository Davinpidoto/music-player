#!/bin/bash

source /home/pi/.virtualenvs/music-player/bin/activate
export PYTHONPATH=/home/pi/music-player
nohup python /home/pi/music-player/music_player/main.py &
