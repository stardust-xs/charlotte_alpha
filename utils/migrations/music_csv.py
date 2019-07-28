"""
Charlotte Music CSV Builder Module
==================================

This module creates CSV of Music files and its metadata.

The module encapsulates below metadata:
    - track_name              : Original file name in local disk
    - title                   : Original title of the music
    - artist                  : Artist of the music
    - albumartist             : Album artist OR Collaborator
    - composer                : Composer of the music
    - album                   : Album name
    - genre                   : Genre of the music
    - duration                : Duration of the music
    - year                    : Release year of the music
    - filesize                : Size of the music on local disk
    - bitrate                 : Bitrate of the music
    - samplerate              : Sample rate OR Frequency
    - disc/track              : Track number
    - disc_total/track_total  : Total tracks in the album
    - comment                 : Comments

See https://github.com/xames3/charlotte for cloning the repository.
"""
from datetime import timedelta
from os import walk
from os.path import join

from hurry.filesize import size, alternative

from tinytag import TinyTag

from charlotte.utils.helpers.common import csv_writer
from charlotte.utils.paths.directories import local_dir
from charlotte.utils.paths.files import ai_file

for _, _, files in walk(local_dir['music']):
    for file in files:
        music_file = TinyTag.get(join(local_dir['music'], file))
        track_name = file
        title = music_file.title
        artist = music_file.artist
        albumartist = music_file.albumartist
        composer = music_file.composer
        album = music_file.album
        genre = music_file.genre
        duration = str(timedelta(seconds=round(music_file.duration)))
        year = music_file.year
        filesize = size(music_file.filesize, system=alternative)
        bitrate = music_file.bitrate
        samplerate = music_file.samplerate
        disc = music_file.disc
        disc_total = music_file.disc_total
        track = music_file.track
        track_total = music_file.track_total
        comment = music_file.comment

        csv_writer(ai_file['music'], track_name, title, artist, albumartist,
                   composer, album, genre, duration, year, filesize, bitrate,
                   samplerate, disc, disc_total, track, track_total, comment)
