"""
The migrate module: Provides functions that are used for migrating data.

These functions helps to perform data creation or data migration related
activities with relative ease. As of now, only music migration is done using
this module. Once I start using Grakn.AI for all database related activities,
these functions will be deprecated.

At a glance, the structure of the module is following:
- migrate_music():      Creates a csv file of the Music files and it`s related
                        metadata. This process is a stepping stone for
                        creating a pre-dataset before moving on completely to
                        Grakn.AI. Once I start using Grakn.AI, this function
                        will most likely be deprecated. The CSV is stored
                        under the `./data/knowledge/csv/` directory.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info

from charlotte.utils.actions.music import
from charlotte.utils.assists.generic import write_to_csv
from charlotte.utils.paths.directories import local_dir
from charlotte.utils.paths.files import ai_file


def migrate_music(file_dir: str = local_dir['music']) -> None:
    """Creates csv of music files.

    file_dir: Directory which hosts music files.
              Default: `D:/Music/` directory.

    Creates a csv file of the Music files and it`s related metadata. This
    process is a stepping stone for creating a pre-dataset before moving on
    completely to Grakn.AI.

    Note: Once I start using Grakn.AI, this function will most likely be
    deprecated. The CSV is stored under the `./data/knowledge/csv/` directory.
    Here are some of the useful metadata information that the function returns:
            * music_file            - File name on local disk
            * track_name            - Actual title of the music track
            * track_artist          - Artist of the music track
            * track_albumartist     - Album artist OR Collaborator of the track
            * track_composer        - Composer of the music track
            * track_album           - Album name
            * track_genre           - Genre of the music track
            * track_duration        - Duration of the music track
            * track_year            - Release year of the music track
            * track_filesize        - Size of the music on local disk
    """
    from os import remove, walk
    from os.path import isfile, join

    try:
        # List of all headers in the csv file.
        header_list = ['music_file', 'track_name', 'track_artist',
                       'track_albumartist', 'track_composer', 'track_album',
                       'track_genre', 'track_duration', 'track_year',
                       'track_filesize']
        # Deletes if the previous csv file exists.
        # This is to avoid data duplication.
        if isfile(ai_file['music']):
            remove(ai_file['music'])
        for _, _, files in walk(file_dir):
            for file in files:
                # Extracting metadata information from the music files and
                # writing it in csv file.
                music_file, track_name, track_artist, track_albumartist, track_composer, track_album, track_genre, track_duration, track_year, track_filesize = extract_metadata(
                    join(local_dir['music'], file))
                write_to_csv(ai_file['music'], music_file, track_name,
                             track_artist, track_albumartist, track_composer,
                             track_album, track_genre, track_duration,
                             track_year, track_filesize)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
