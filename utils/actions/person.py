"""
This module hosts set of functions related to the user OR helps defining the
user attributes.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info

from charlotte.utils.profiles.default import title


def wish_user() -> str:
    """
    Definition
    ----------
        Wishes the user Good Morning/Evening based on the time of the day.

    Returns
    -------
        greeting : string, default
            Respective timezone greeting.
    """
    from datetime import datetime
    from random import choice

    hour = datetime.now().hour
    morning = choice([f'Good Morning, {title}.', 'Good Morning!'])
    afternoon = choice([f'Good Afternoon, {title}.', 'Good Afternoon!'])
    evening = choice([f'Good Evening, {title}.', 'Good Evening!'])
    night = choice(
        [f'Hello, {title}!', f'Oh hello, {title}!', f'Welcome back, {title}.'])
    greeting = morning if hour >= 5 and hour < 12 else afternoon if hour >= 12 and hour < 17 else evening if hour >= 17 and hour < 22 else night
    return greeting


def age(birthdate: str) -> int:
    """
    Definition
    ----------
        Calculates the age based on the birthdate provided.
        It just provides years and not months.

    Parameter
    ---------
        birthdate : string, mandatory
            Birthdate in string format. The birthdate needs to be ISO 8601
            format (For e.g. `1995-05-31`).

    Returns
    -------
        age : integer, default
            Returns age in integer format.

    Notes
    -----
        This age calculation is used while building profile.
    """
    from datetime import date

    try:
        days_in_year = 365.2425
        year = int(birthdate.split('-')[0])
        month = int(birthdate.split('-')[1])
        day = int(birthdate.split('-')[2])
        age = int((date.today() - date(year, month, day)).days / days_in_year)
        return age
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


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

    try:
        gmaps = Client(key=os.environ.get('CHARLOTTE_MAPS_KEY'))
        current_coords = gmaps.geolocate()
        location = osm(
            list(current_coords['location'].values()), method='reverse')
        if area is not None:
            try:
                return location.json[area]
            except:
                return 'null'
        else:
            try:
                return location.json['address']
            except:
                return 'null'
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')
