"""
This module hosts functions that are used for creating OR migrating data.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info

from charlotte.utils.paths.directories import local_dir
from charlotte.utils.paths.files import ai_file
from charlotte.utils.assists.generic import csv_writer
from charlotte.utils.actions.music import music_metadata_extractor


def migrate_music(file_dir: str = local_dir['music']) -> None:
    """
    Definition
    ----------
        Creates a CSV of Music files and its metadata.
        The CSV is stored under the `./data/knowledge/csv/` directory.

    Parameter
    ---------
        file_dir : string, mandatory
            Directory which has music files.
            Global default: `D:/Music/` directory.

    Notes
    -----
        The module encapsulates below metadata:
            music_file              : Original file name in local disk
            track_name              : Original title of the music
            track_artist            : Artist of the music
            track_albumartist       : Album artist OR Collaborator
            track_composer          : Composer of the music
            track_album             : Album name
            track_genre             : Genre of the music
            track_duration          : Duration of the music
            track_year              : Release year of the music
            track_filesize          : Size of the music on local disk
    """
    from os import remove, walk
    from os.path import isfile, join

    header_list = ['music_file', 'track_name', 'track_artist',
                   'track_albumartist', 'track_composer', 'track_album',
                   'track_genre', 'track_duration', 'track_year',
                   'track_filesize']
    if isfile(ai_file['music']):
        remove(ai_file['music'])
    for _, _, files in walk(file_dir):
        for file in files:
            music_file, track_name, track_artist, track_albumartist, track_composer, track_album, track_genre, track_duration, track_year, track_filesize = music_metadata_extractor(
                join(local_dir['music'], file))
            csv_writer(ai_file['music'], music_file, track_name, track_artist,
                       track_albumartist, track_composer, track_album,
                       track_genre, track_duration, track_year,
                       track_filesize)
