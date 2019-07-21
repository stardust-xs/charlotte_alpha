"""
Charlotte`s actions assistant
=============================

It provides assistance to simplify actions.

See https://github.com/xames3/charlotte for complete documentation.
"""
from . basics import display
from .. fluids.paths import PATH


def age(birthdate: str) -> int:
    """
    Definition
    ----------
        Calculates the age based on the birthdate provided.

    Parameter
    ---------
        birthdate : string, mandatory
            Birthdate in string format. The birthdate needs to be ISO 8601
            format.

    Returns
    -------
        age : integer, default
            Returns age in integer format.

    Notes
    -----
        This age calculation is used while building profile.
    """
    from datetime import date

    days_in_year = 365.2425
    year = int(birthdate.split('-')[0])
    month = int(birthdate.split('-')[1])
    day = int(birthdate.split('-')[2])
    age = int((date.today() - date(year, month, day)).days / days_in_year)
    return age


def locate(area: str = None) -> str:
    """
    Definition
    ----------
        Returns current location using reverse lookup via Google Maps API.

    Parameter
    ---------
        area : string, optional
            Looks for specific details of an address while locating.
            Global default: False

    Returns
    -------
        Depending upon passed value, function returns specific address related
        information.

    Notes
    -----
        Function uses Google Maps for retreiving latitude and longitude using
        Google Maps API. Hence it is necessary to generate the API key.
        You can generate it here: `https://console.developers.google.com`
    """
    import os
    from geocoder import osm
    from googlemaps import Client

    gmaps = Client(key=os.environ.get('CHARLOTTE_MAPS'))
    current_coords = gmaps.geolocate()
    location = osm(list(current_coords['location'].values()), method='reverse')
    if area is not None:
        try:
            return location.json[area]
        except:
            return 'NA'
    else:
        try:
            return location.json['address']
        except:
            return 'NA'


def find(file: str, file_dir: str, min_score: int = 65) -> tuple:
    """
    Definition
    ----------
        Finds the matching file in the directory.

    Parameters
    ----------
        file : string, mandatory
            Name of the file you need to search in the directory.
            The name can be fuzzy.

        file_dir : string, mandatory
            Directory in which the file exists or needs to be searched in.

        min_score : integer, optional
            Minimum score/Threshold score that should match while making as
            approximate guess.
            Global default: 65

    Returns
    -------
        actual_file[0], current_score : tuple, default
            Returns correctly guessed file name with matching score.
    """
    from os import walk
    from fuzzywuzzy import fuzz, process

    for root, _, files in walk(file_dir):
        guessed_files = process.extract(
            file, files, limit=3, scorer=fuzz.partial_ratio)
        no_match_score = 0
        no_match_found = f'Sorry, I could\'nt find \'{file}\' in the directory.'
        for actual_file in guessed_files:
            current_score = fuzz.partial_ratio(file, actual_file)
            if current_score > min_score and current_score > no_match_score:
                return actual_file[0], current_score
            else:
                return no_match_found, no_match_score


def play_music(file: str = None, file_dir: str = PATH['music']) -> None:
    """
    Definition
    ----------
        Plays music from `D:/Music` directory.

    Parameters
    ----------
        file : string, mandatory
            Name of the file you need to search in the directory.
            The name can be fuzzy.

        file_dir : string, mandatory
            Directory in which the file exists or needs to be searched in.
            Here, it`s under Music directory.
            Global default: D:/Music/
    """
    from os import startfile, listdir
    from os.path import isfile, join
    from random import choice

    if file is not None:
        file_name, file_score = find(file, file_dir)
        if file_score == 0:
            return file_name
        else:
            music_file = join(file_dir, file_name)
            startfile(f'{music_file}')
    else:
        random_file = choice([join(PATH['music'], file) for file in listdir(
            PATH['music']) if isfile(join(PATH['music'], file))])
        startfile(random_file)
