"""
The music module: Provides functions for music related operations.

These functions help with playing music or handling data related to music
files. The `migrate_music` function is soon to be deprecated and is about to be
replaced by use of graph dB, Grakn.AI.

At a glance, the structure of the module is following:
 - migrate_music():     Creates a csv file of the Music files and it`s related
                        metadata. This process is a stepping stone for
                        creating a pre-dataset before moving on completely to
                        Grakn.AI. Once the use of Grakn is started, this
                        function will most likely be deprecated. The CSV is
                        stored under the `./data/knowledge/csv/` directory.
 - play_music_using_metadata(): Similar to `_play_music` function but instead
                        of playing music from given music file, it plays using
                        the metadata references from the csv file. The use of
                        csv file for pulling information will soon get
                        deprecated and will be replaced with Grakn.AI.
 - reply_on_playing():  Returns a response of the played track name.
                        This response is displayed during the inference.
 - play_next_track():   Plays next track in queue. This makes sure there is
                        always something to play if next track is requested.
 - play_previous_track(): Plays previous track.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   1.0.2 - Fixed error caused when `os.walk` was not imported in
#           `play_music_using_metadata` function.
#           Added ignored support for previous and next track in
#           `play_music_using_metadata` function.
#           Added support for fuzzy finder while finding the previous and next
#           tracks from the track_list in `play_music_using_metadata`.
#           Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info

from charlotte.utils.assists.generic import find_file, str_match, write_to_csv
from charlotte.utils.assists.profile import lower, title
from charlotte.utils.assists.system import minimize_window
from charlotte.utils.paths.directories import local_dir
from charlotte.utils.paths.files import ai_file

# Constant used by `play_music_using_metadata` to use default UTF-8 encoding.
_ENCODING = 'utf-8'


def _extract_metadata(file: str) -> tuple:
    """Extracts music metadata.

    file: Music file name whose metadata needs to be extracted.

    Extracts the metadata of the music files. This metadata is required to
    provide necessary information and is recommended to use in conjunction
    with function `play_music_using_metadata`.
    """
    from os.path import basename, isfile
    from datetime import timedelta
    from hurry.filesize import size, alternative
    from tinytag import TinyTag

    try:
        # Execute code if file exists.
        if isfile(file):
            music_track = TinyTag.get(file)
            music_file = basename(file)
            track_name = music_track.title
            track_artist = music_track.artist
            track_albumartist = music_track.albumartist
            track_composer = music_track.composer
            track_album = music_track.album
            track_genre = music_track.genre
            track_duration = str(
                timedelta(seconds=round(music_track.duration)))
            track_year = music_track.year
            track_filesize = size(music_track.filesize, system=alternative)
            # Returns all the extracted metadata along with music filename.
            return music_file, track_name, track_artist, track_albumartist, track_composer, track_album, track_genre, track_duration, track_year, track_filesize
        else:
            return f'Sorry {lower}. I could not find any track with the search parameters.'
    except Exception as error:
        exception(error)


def migrate_music(file_dir: str = local_dir['music']) -> None:
    """Creates csv of music files.

    file_dir: Directory which contains music files.
              Default: `D:/Music/` directory.

    Creates a csv file of the Music files and it`s related metadata. This
    process is a stepping stone for creating a pre-dataset before moving on
    completely to Grakn.AI.

    Note: Here are some of the useful metadata information that the function
    returns:
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

    Caution: Once the use of Grakn.AI is started, this function will most
    likely be deprecated. The CSV is stored under the `./data/knowledge/csv/`
    directory.
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
                music_file, track_name, track_artist, track_albumartist, track_composer, track_album, track_genre, track_duration, track_year, track_filesize = _extract_metadata(
                    join(local_dir['music'], file))
                # Writing it in csv file.
                write_to_csv(ai_file['music'], music_file, track_name,
                             track_artist, track_albumartist, track_composer,
                             track_album, track_genre, track_duration,
                             track_year, track_filesize)
    except Exception as error:
        exception(error)


def _play_music(file: str = None, file_dir: str = local_dir['music']) -> None:
    """Plays music.

    file:     Fuzzy name of the music file that needs to be played.
              Default: None
    file_dir: Directory which has music files.
              Here, it`s under Music directory.
              Default: D:/Music/

    Plays music from default music directory, `D:/Music/`.

    Note: If no music selection/file is provided, the function will start
    playing music automatically at random from the default music directory.
    """
    from os import startfile, listdir
    from os.path import isfile, join
    from random import choice

    try:
        # If music file name is provided then play that music file, else play
        # any random music file from the default music directory.
        if file:
            # This returns a tuple with file name and it`s score.
            # For more information on the function, refer generic.py module.
            file_name, file_score = find_file(file, file_dir)
            if file_score == 0:
                return file_name
            else:
                music_file = join(file_dir, file_name)
        else:
            # Randomly chooses file from the default music directory.
            music_file = choice([join(local_dir['music'], file) for file in listdir(
                local_dir['music']) if isfile(join(local_dir['music'], file))])
        # Plays the music file.
        startfile(music_file)
        minimize_window('Groove Music')
        return _extract_metadata(music_file)
    except Exception as error:
        exception(error)


def play_music_using_metadata(music_file: str = None,
                              track_name: str = None,
                              track_artist: str = None,
                              track_albumartist: str = None,
                              track_composer: str = None,
                              track_album: str = None,
                              track_genre: str = None,
                              track_duration: str = None,
                              track_year: str = None,
                              track_filesize: str = None) -> None:
    """Plays music using references.

    music_file:        Name of the music file you need to search in csv file.
    track_name:        Name of the track.
    track_artist:      Name of the artist.
    track_albumartist: Name of the artist/s which featured in the track.
    track_composer:    Name of the composer.
    track_album:       Name of the album.
    track_genre:       Name of the music genre.
    track_duration:    Music file duration.
    track_year:        Year in which the track was released.
    track_filesize:    Music file size (in MBs).

    Similar to `_play_music` function but instead of playing music from given
    music file, it plays using the metadata references from the csv file.

    Note: The use of csv file for pulling information will soon get deprecated
    and will be replaced with Grakn.AI.

    Caution: All values are None by default. This will ensure, no value is
    passed to the `_play_music` function inside it. No input to `_play_music`
    will play file randomly.
    """
    from os import walk
    from random import randint
    from numpy import ones
    from pandas import read_csv, Series

    try:
        # Generating a list of all the tracks inside the directory.
        for _, _, track_list in walk(local_dir['music']):
            pass
        # If music file is given, find it`s relative previous and next track.
        if music_file:
            # This generated track list is used for finding the relative next
            # and previous tracks.
            previous_track = track_list[track_list.index(
                str_match(music_file, track_list)) - 1]
            next_track = track_list[track_list.index(
                str_match(music_file, track_list)) + 1]
            playing_file = _play_music(music_file)
            return playing_file, previous_track, next_track
        elif track_name:
            # Added support for previous and next track since the inputs come
            # from a Slot, track_name.
            previous_track = track_list[track_list.index(
                str_match(track_name, track_list)) - 1]
            next_track = track_list[track_list.index(
                str_match(track_name, track_list)) + 1]
            playing_file = _play_music(track_name)
            return playing_file, previous_track, next_track
        else:
            music_csv_file = ai_file['music']
            # Calling csv object for lookup.
            df = read_csv(music_csv_file, encoding=_ENCODING)
            # Creating a master dictionary which has all the filtering
            # parameters from the given arguments, including None values.
            master_dict = {
                'track_name': str_match(track_name, df['track_name'].dropna().tolist()),
                'track_artist': str_match(track_artist, df['track_artist'].dropna().tolist()),
                'track_albumartist': str_match(track_albumartist, df['track_albumartist'].dropna().tolist()),
                'track_composer': str_match(track_composer, df['track_composer'].dropna().tolist()),
                'track_album': str_match(track_album, df['track_album'].dropna().tolist()),
                'track_genre': str_match(track_genre, df['track_genre'].dropna().tolist()),
                'track_duration': str_match(track_duration, df['track_duration'].dropna().tolist()),
                'track_year': str_match(track_year, df['track_year'].dropna().tolist()),
                'track_filesize': str_match(track_filesize, df['track_filesize'].dropna().tolist())}
            # Creating a filtered dictionary with only non-None key-value pair.
            filtered_dict = {k: v for k,
                             v in master_dict.items() if v is not None}
            # Not sure what it does, referred from the internet.
            # Link to the reference code is to be posted here.
            filter_series = Series(ones(df.shape[0], dtype=bool))
            for column, value in filtered_dict.items():
                filter_series = ((df[column] == value) & filter_series)
            # Generating track list which is used for finding the relative next
            # and previous tracks from the filtered dictionary.
            track_list = df[filter_series]['music_file'].tolist()
            if len(df[filter_series]) > 1:
                # If more than one track is returned after applying all the
                # filters, it picks music file at random along with returning
                # previous and next tracks.
                random_pick = df[filter_series].iloc[randint(
                    0, len(df[filter_series])), 0]
                previous_track = track_list[track_list.index(random_pick) - 1]
                next_track = track_list[track_list.index(random_pick) + 1]
                playing_file = _play_music(random_pick)
                return playing_file, previous_track, next_track
            elif len(df[filter_series]) == 1:
                # If only one value is received after applying all filters.
                current_pick = df[filter_series].iloc[0, 0]
                previous_track = track_list[track_list.index(current_pick) - 1]
                next_track = track_list[track_list.index(current_pick) + 1]
                playing_file = _play_music(current_pick)
                return playing_file, previous_track, next_track
            else:
                return f'Sorry {lower}. I could not find any track with the search parameters.'
    except Exception as error:
        exception(error)


def reply_on_playing(file_name: str = None,
                     track_name: str = None,
                     track_artist: str = None) -> None:
    """Returns track response.

    file_name:    Name of the music file.
    track_name:   Name of the music track.
    track_artist: Name of the artist.

    Returns a response of the played track name. This response is displayed
    during the inference.

    Caution: All values are None by default.
    """
    from pathlib import Path
    from random import choice

    # Returns file name without extension.
    file_name = Path(file_name).stem
    with_file_name = [f'Alright, playing {file_name}.',
                      f'Alright {lower}, playing {file_name}.',
                      f'Sure, playing {file_name}.',
                      f'Okay, playing {file_name}.',
                      f'Right on it, {lower}.',
                      'Here you go...',
                      'Okay...']
    with_track_name = [f'Alright, playing {track_name}.',
                       f'Alright {lower}, playing {track_name}.',
                       f'Sure, playing {track_name}.',
                       f'Okay, playing {track_name}.',
                       f'Right on it, {lower}.',
                       'Here you go...',
                       'Okay...']
    both_details = [f'Alright, playing {track_name} by {track_artist}.',
                    f'Alright, playing {track_name}.',
                    f'Alright {lower}, playing {track_name}.',
                    f'Sure, playing {track_name} by {track_artist}.',
                    f'Okay, playing {track_name} by {track_artist}.',
                    f'Right on it, {lower}.',
                    'Okay...']

    without_file_name = [f'Sorry {lower}. I could not find any track with '
                         'the search parameters.',
                         f'Sorry {lower}. I could not find any match for'
                         ' the playing track.']
    try:
        # If no track is detected after passing multiple parameters and random
        # is not played, it returns below choice.
        if len(file_name) == 1 and file_name == 'S':
            return choice(without_file_name)
        else:
            # If valid details are provided, it returns respective choice.
            if track_artist is None:
                if track_name is None:
                    return choice(with_file_name)
                else:
                    return choice(with_track_name)
            else:
                return choice(both_details)
    except Exception as error:
        exception(error)


def play_next_track(next_track: str) -> None:
    """Plays next track.

    next_track: Name of the next track to play.

    Plays next track in queue. This makes sure there is always something to
    play if next track is requested.
    """
    try:
        # If no input is given, it will return no track to play response.
        if next_track is None:
            return f'Sorry {lower}. There is no track to play.'
        else:
            return play_music_using_metadata(music_file=next_track,
                                             track_name=next_track)
    except Exception as error:
        exception(error)


def play_previous_track(previous_track: str) -> None:
    """Plays previous track.

    previous_track: Name of the previous track to play.

    Similar to `play_next_track`, plays previous track relative to the current
    track.
    """
    try:
        # If no input is given, it will return no track to play response.
        if previous_track is None:
            return f'Sorry {lower}. There is no track to play.'
        else:
            return play_music_using_metadata(music_file=previous_track,
                                             track_name=previous_track)
    except Exception as error:
        exception(error)
