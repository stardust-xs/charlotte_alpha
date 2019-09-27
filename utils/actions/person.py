"""
The person module: Provides functions related to the user.

These functions help to perform user level requests.

At a glance, the structure of the module is following:
 - greet_user():        Greets the user based on time of the day and returns
                        current time, current hour and minutes. These
                        responses needs to be expanded in future. The time is
                        calculated on the basis of the current hour.
 - age():               Calculates the age based on the given date. This
                        function calculates the time delta between today and
                        the given date and returns age in integer.
 - locate():            Find and returns current global position using reverse
                        lookup via Google Maps API. Function uses Google Maps
                        for retreiving latitude and longitude using Google
                        Maps API. Hence it is necessary to generate the API
                        key first before running this function.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.6 - `greet_user` function now uses new dictionaries.
#   1.0.5 - `wish_user` is now changed to `greet_user` and fixed typos in it.
#           `greet_user` function now returns current time, hour and minutes.
#   1.0.4 - `locate` function now uses `check_internet` to check if internet
#           connection is available or not.
#   1.0.2 - Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info

from charlotte.utils.assists.generic import timestamp
from charlotte.utils.assists.phrases import greetings_protocol
from charlotte.utils.assists.profile import title
from charlotte.utils.assists.system import check_internet

# Constant used by `greet_user` to define hour for dawn.
_MORNING = 5
# Constant used by `greet_user` to define hour for noon.
_NOON = 12
# Constant used by `greet_user` to define hour for evening.
_EVENING = 17
# Constant used by `greet_user` to define hour for night.
_NIGHT = 21
# Constant used by `age` to define the total days in a year.
_DAYS_IN_YEAR = 365.2425
# Constant used by `locate` to return if no response is returned.
_NO_RESPONSE = 'null'


def greet_user() -> str:
    """Greets user.

    Greets the user based on time of the day and returns current time (in
    24hr format), current hour and minutes.

    Note: These responses needs to be expanded in future. The time is
    calculated on the basis of the current hour.
    """
    from datetime import datetime
    from random import choice

    # Calculates current hour and minutes.
    time = datetime.now().strftime(timestamp('%H:%M'))
    hour = datetime.now().hour
    minutes = datetime.now().minute
    morning = choice(greetings_protocol['morning'])
    afternoon = choice(greetings_protocol['afternoon'])
    evening = choice(greetings_protocol['evening'])
    night = choice(greetings_protocol['night'])
    # Determining which greeting should be used.
    greeting = morning if hour >= _MORNING and hour < _NOON else afternoon if hour >= _NOON and hour < _EVENING else evening if hour >= _EVENING and hour < _NIGHT else night
    # Returns greetings as per the day and returns current time-hour-minutes.
    return greeting, time, hour, minutes


def age(birthdate: str) -> int:
    """Calculates age.

    birthdate: Birthdate in string format.

    Calculates the age based on the given date. This function calculates the
    time delta between today and the given date and returns age in integer.

    Note: The birthdate needs to be ISO 8601 format (For e.g. 1995-05-31).
    It just provides years and not months.
    """
    from datetime import date

    try:
        year = int(birthdate.split('-')[0])
        month = int(birthdate.split('-')[1])
        day = int(birthdate.split('-')[2])
        age = int((date.today() - date(year, month, day)).days / _DAYS_IN_YEAR)
        return age
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def locate(area: str = None) -> str:
    """Returns current location.

    area: Looks for specific details of an address while locating.
          Default: None

    Find and returns current global position using reverse lookup via Google Maps API.

    Note: Function uses Google Maps for retreiving latitude and longitude
    using Google Maps API. Hence it is necessary to generate the API key first
    before running this function.
    You can generate it here: https://console.developers.google.com

    Caution: If you run the function without passing valid API key, it will
    raise an exception.
    """
    import os
    from geocoder import osm
    from googlemaps import Client

    try:
        if check_internet():
            # Passing Google maps API key.
            gmaps = Client(key=os.environ.get('CHARLOTTE_MAPS_KEY'))
            # Finding current latitude and longitude details.
            current_coords = gmaps.geolocate()
            location = osm(
                list(current_coords['location'].values()), method='reverse')
            if area is not None:
                try:
                    # Returns particular address detail only.
                    return location.json[area]
                except:
                    return _NO_RESPONSE
            else:
                try:
                    # Returns complete address.
                    return location.json['address']
                except:
                    return _NO_RESPONSE
        else:
            # Returns None if no internet connection is available.
            return None
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
