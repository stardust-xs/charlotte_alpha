"""
This module packs set of functions related to playing music OR handling data
related to music files.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info

from charlotte.utils.actions.generic import find, string_match
from charlotte.utils.paths.directories import local_dir
from charlotte.utils.paths.files import ai_file
from charlotte.utils.profiles.user import title


def music_metadata_extractor(file: str) -> tuple:
    """
    Definition
    ----------
        Extracts the metadata from music files.

    Parameters
    ----------
        file : string, mandatory
            Name of the file you need to search in the directory.

    Returns
    -------
        music_file : string, default
        track_name : string, default
        track_artist : string, default
        track_albumartist : string, default
        track_composer : string, default
        track_album : string, default
        track_genre : string, default
        track_duration : string, default
        track_year : string, default
        track_filesize : string, default
            Metadata of the music file.
    """
    from os.path import basename
    from datetime import timedelta
    from hurry.filesize import size, alternative
    from tinytag import TinyTag

    try:
        music_track = TinyTag.get(file)
        music_file = basename(file)
        track_name = music_track.title
        track_artist = music_track.artist
        track_albumartist = music_track.albumartist
        track_composer = music_track.composer
        track_album = music_track.album
        track_genre = music_track.genre
        track_duration = str(timedelta(seconds=round(music_track.duration)))
        track_year = music_track.year
        track_filesize = size(music_track.filesize, system=alternative)

        return music_file, track_name, track_artist, track_albumartist, track_composer, track_album, track_genre, track_duration, track_year, track_filesize
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def play_music(file: str = None, file_dir: str = local_dir['music']) -> None:
    """
    Definition
    ----------
        Plays music from `D:/Music` directory.

    Parameters
    ----------
        file : string, mandatory
            Name of the music file you need to search in the directory.
            Global default: None

        file_dir : string, mandatory
            Directory in which the file exists or needs to be searched in.
            Here, it`s under Music directory.
            Global default: D:/Music/
    """
    from os import startfile, listdir
    from os.path import isfile, join
    from pathlib import Path
    from random import choice

    try:
        if file is not None:
            file_name, file_score = find(file, file_dir)
            if file_score == 0:
                return file_name
            else:
                music_file = join(file_dir, file_name)
                startfile(music_file, operation=None)
                played_file = music_metadata_extractor(music_file)
                if played_file[1] is None:
                    return Path(music_file).stem
                else:
                    return played_file[1]
        else:
            music_file = choice([join(local_dir['music'], file) for file in listdir(
                local_dir['music']) if isfile(join(local_dir['music'], file))])
            startfile(music_file)
            played_file = music_metadata_extractor(music_file)
            if played_file[1] is None:
                return Path(music_file).stem
            else:
                return played_file[1]
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def play_music_by_attribute(music_file: str = None,
                            track_name: str = None,
                            track_artist: str = None,
                            track_albumartist: str = None,
                            track_composer: str = None,
                            track_album: str = None,
                            track_genre: str = None,
                            track_duration: str = None,
                            track_year: str = None,
                            track_filesize: str = None) -> None:
    """
    Definition
    ----------
        Plays music after pulling information from CSV file under
        `./data/knowledge/csv/music.csv`.

    Parameters
    ----------
        music_file : string, optional
            Name of the music file you need to search in the CSV file.
            Global default: None

        track_name : string, optional
            Name of the track.
            Global default: None

        track_artist : string, optional
            Name of the artist.
            Global default: None

        track_albumartist : string, optional
            Name of the artist/s which featured in the track.
            Global default: None

        track_composer : string, optional
            Name of the composer.
            Global default: None

        track_album : string, optional
            Name of the album.
            Global default: None

        track_genre : string, optional
            Name of the music genre.
            Global default: None

        track_duration : string, optional
            Music file duration.
            Global default: None

        track_year : string, optional
            Year in which the track was released.
            Global default: None

        track_filesize : string, optional
            Music file size (in MBs).
            Global default: None

    Notes
    -----
        This function used data from the CSV file. Later it will be replaced
        by a Graph DB like Grakn.AI.
    """
    from random import randint
    from numpy import ones
    from pandas import read_csv, Series

    try:
        if music_file is not None:
            played_file = play_music(music_file)
            return played_file
        else:
            music_csv_file = ai_file['music']
            df = read_csv(music_csv_file, encoding='utf-8', )
            master_dict = {
                'track_name': string_match(track_name, df['track_name'].dropna().tolist()),
                'track_artist': string_match(track_artist, df['track_artist'].dropna().tolist()),
                'track_albumartist': string_match(track_albumartist, df['track_albumartist'].dropna().tolist()),
                'track_composer': string_match(track_composer, df['track_composer'].dropna().tolist()),
                'track_album': string_match(track_album, df['track_album'].dropna().tolist()),
                'track_genre': string_match(track_genre, df['track_genre'].dropna().tolist()),
                'track_duration': string_match(track_duration, df['track_duration'].dropna().tolist()),
                'track_year': string_match(track_year, df['track_year'].dropna().tolist()),
                'track_filesize': string_match(track_filesize, df['track_filesize'].dropna().tolist())}

            filtered_dict = {k: v for k,
                             v in master_dict.items() if v is not None}
            filter_series = Series(ones(df.shape[0], dtype=bool))
            for column, value in filtered_dict.items():
                filter_series = ((df[column] == value) & filter_series)

            if len(df[filter_series]) > 1:
                random_pick = df[filter_series].iloc[randint(
                    0, len(df[filter_series])), 0]
                played_file = play_music(random_pick)
                return played_file
            elif len(df[filter_series]) == 1:
                played_file = play_music(df[filter_series].iloc[0, 0])
                return played_file
            else:
                return f'Sorry, {title}. I couldn\'t find any combination of'
                ' the search parameters. Please try using different keywords.'
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def music_responder(music_file: str = None,
                    track_name: str = None,
                    track_artist: str = None,
                    track_albumartist: str = None,
                    track_composer: str = None,
                    track_album: str = None,
                    track_genre: str = None,
                    track_duration: str = None,
                    track_year: str = None,
                    track_filesize: str = None) -> None:
    pass
