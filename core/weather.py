"""
The weather module: Provides weather forecast.

These module lets you to perform weather forecast related queries with
relative ease.

At a glance, the structure of the module is following:
 - forecast():          Returns the weather forecast. This is done using
                        API call made to `DarkSky.net`. It can return
                        current weather and/or forecast on basis of days
                        or hours. An account on `https://darksky.net/`
                        is required to get the api key. API call is made
                        to retreive the weather report. Only 1000 calls
                        be made per month on the free tier.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   1.1.1 - Updated entire script.
#           Made the code more* PEP-8 compliant.
#           Profiled and optimized using `profiler`.
#           Improved the type hints by using the typing module.
#           Removed _current, _predict and weather_event and replaced
#           them with `forecast` function.
#           Added support for finding the coords within weather.py
#           instead of importing function from person.py module.
#           Added new functions for getting coords - _get_coords,
#                               for wind direction - _wind_dir and
#                               for part of the day - _part_day
#   1.1.0 - Added new constants for supporting weather retreival in
#           Imperial metric system.
#           `_current` and `_predict` now replaces previous functions
#           for better support and integration.
#           `weather_event` now replaces `current_forecast_weather`.
#           `_predict()` now has more natural responses for weather
#           predictions.
#   1.0.7 - Fixed typo in `current_weather` function.
#   1.0.6 - All functions now return None if internet is not available.
#   1.0.4 - `current_weather` and `forecast_weather` function now uses
#           `check_internet` to check if internet is available.
#           'current_forecast_weather' now also returns None if no
#           internet is detected.
#           Added internal comments while returning None in all
#           functions.
#   1.0.3 - All functions return None if any exception is raised.
#   1.0.2 - Fixed error caused by redundant quotes in `forecast_weather`
#           function.
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info
from typing import Optional, Text, Tuple, Union

from charlotte.utils.assists.constants import DARK, DAWN, DUSK, NOON
from charlotte.utils.assists.system import check_internet, resolve_days


def _get_coords(location: Optional[Text] = None) -> Tuple:
    """Returns coords for the asked location.

    location: Location or the address to be converted to latitude and
              longitude.
              Default: None

    Find and returns current global position and the city using reverse
    lookup via Google Maps API.

    Note: Function uses Google Maps for retreiving latitude & longitude
    using it`s API. Hence it is necessary to generate the API key first
    before running this function.
    You can generate it here: https://console.developers.google.com

    Caution: If you run the function without passing valid API key, it
    will raise an exception.
    """
    import os
    from geocoder import osm
    from googlemaps import Client

    try:
        # Passing Google maps API key.
        map = Client(key=os.environ.get('CHARLOTTE_MAPS_KEY'))
        # Finding current latitude and longitude coordinates.
        if location:
            curr = map.geocode(location)
            coords = (curr[0]['geometry']['location']['lat'],
                      curr[0]['geometry']['location']['lng'])
        else:
            curr = map.geolocate()
            coords = (curr['location']['lat'],
                      curr['location']['lng'])
        # Reverse mapping the coordinates to find out the city name.
        area = osm(coords, method='reverse')
        loc_list = ['city', 'town', 'suburb', 'state', 'region', 'country']
        for idx in loc_list:
            if area.json.get(idx, None) is not None:
                loc = area.json[idx]
                break
        return coords, loc
    except Exception as error:
        print('An error occured while performing this operation because of '
              f'{error} in function "{stack()[0][3]}" on line '
              f'{exc_info()[-1].tb_lineno}.')
        return (None, None), None


def _wind_dir(degree: Union[float, int]) -> Text:
    """Returns direction of the wind.

    degree: The degrees in which which the wind is blowing relative to
            true north.

    Note: If you need more directions to consider, ensure the number of
    elements in the `directions` list matches the number for the modulo
    operator. Here, only 8 directions are considered so dividing by 8.
    """
    directions = ['northern', 'northeastern', 'eastern', 'southeastern',
                  'southern', 'southwestern', 'western', 'northwestern']
    idx = int((degree + 11.25)/22.5)
    return directions[idx % 8]


def _part_day() -> Text:
    """Returns the part of the day.

    Note: If you need to change the hours when each of the timezone
    starts, please have a look at `./utils/assists/constants.py` and
    change it accordingly.
    """
    from datetime import datetime
    from random import choice

    hr = datetime.now().hour
    part = choice(['morning', 'day']) if hr >= DAWN and hr < NOON else \
        choice(['afternoon', 'day']) if hr >= NOON and hr < DUSK else \
        'evening' if hr >= DUSK and hr < DARK else 'night'
    return part


def forecast(location: Optional[Text] = None,
             days: Optional[int] = None,
             hours: Optional[int] = None,
             metric: bool = True) -> Text:
    """Returns weather.

    location: Location where you need to find the weather forecast for.
              This location can be any valid address, city, etc.
              Default: None (Current location)
    days:     Number of days, for which the forecast is needed. Maximum
              7 days forecast is currently possible.
              Default: None (Todays`s forecast)
    hours:    Number of hours, for which the forecast is needed. Maximum
              of 48 hours of forecast is currently possible.
              Default: None (Current weather)
    metric:   Unit metrics to be used, Metric or Imperial.
              Default: True

    Returns the weather. This is done using an API call made to
    `DarkSky.net`. It can return current weather and/or forecast on
    basis of days or hours.

    Note: An account on `https://darksky.net/` is required to get the
    api key. API call is made to retreive the weather report. Only 1000
    calls can be made per month on the free tier.

    Caution: If you run the function without passing valid API key, it
    will raise an exception.
    """
    import os
    from random import choice, shuffle
    from requests import get

    try:
        if check_internet():
            (lat, lng), loc = _get_coords(location)
            key = os.environ.get('CHARLOTTE_DSKY_KEY')
            u, t, s = ('si', '°C', 'kph') if metric else ('us', '°F', 'mph')
            url = f'https://api.darksky.net/forecast/{key}/' \
                  f'{lat},{lng}?units={u}'
            obj = get(url).json()
            if days and days <= 7 and days > 0:
                data, idx = obj['daily']['data'][days], 0
                temp = str(obj['currently']['temperature']) + t
                feel = str(obj['currently']['apparentTemperature']) + t
                max = str(data['apparentTemperatureMax']) + t
                min = str(data['apparentTemperatureMin']) + t
            elif hours and hours <= 48:
                data, idx = obj['hourly']['data'][hours], 1
                temp = str(data['temperature']) + t
                feel = str(data['apparentTemperature']) + t
                max = str(obj['daily']['data'][0]['apparentTemperatureMax']) \
                    + t
                min = str(obj['daily']['data'][0]['apparentTemperatureMin']) \
                    + t
            else:
                data, idx = obj['currently'], 2
                temp = str(obj['currently']['temperature']) + t
                feel = str(obj['currently']['apparentTemperature']) + t
                max = str(obj['daily']['data'][0]['apparentTemperatureMax']) \
                    + t
                min = str(obj['daily']['data'][0]['apparentTemperatureMin']) \
                    + t
            cond = str(data['summary']).lower().strip('.')
            if cond.startswith('possible'):
                cond = cond.replace('possible', 'possible to have') + \
                    ' weather'
            if cond.startswith('rain'):
                cond = cond.replace('rain', 'rainy weather')
            if cond.endswith('cloudy'):
                cond = cond + ' weather'
            if cond.startswith('light'):
                cond = cond.replace('light', 'possible to have light') + \
                    ' weather'
            if cond.startswith('heavy'):
                cond = cond.replace('heavy', 'possible to have heavy') + \
                    ' weather'
            hum = str(data['humidity'] * 100) + '%'
            spd = str(data['windSpeed']) + f' {s}'
            fore = obj['daily']['summary']
            cloud = data['cloudCover']
            deg = data['windBearing']
            sky = 'brighter' if cloud < 0.5 else 'darker'
            dir = _wind_dir(deg)
            part = _part_day()
            day = resolve_days(days)
            pl = 'day' if days == 1 else 'days'
            _days = [f'For the next {days} {pl} there are some places in '
                     f'{loc} that will be {cond}. Interestingly, there would '
                     f'be {fore}',
                     f'Well it does look as if we\'ll see more {cond} across '
                     f'{loc} for the next {days} {pl}. More so there will be '
                     f'{fore}',
                     f'Some parts of {loc} will be seeing a bit of {cond} for '
                     f'the next {days} {pl} with average temperature of {feel}'
                     f'. But for the most part it\'ll fluctuate between {max} '
                     f'high & {min} low.',
                     f'Well for the next {days} {pl}, it seems it\'ll be '
                     f'fairly {cond} in some parts of {loc}. Winds can be '
                     f'seen gushing at speeds upto {spd} and as we go '
                     'through the week the temperature will vary between '
                     f'{max} high & {min} low.',
                     f'I could see some {sky} skies over {dir} parts of {loc} '
                     f'for the next {days} {pl}. Also we do have some {cond} '
                     'spells with the temperature struggling to be '
                     f'about {temp}.',
                     f'For {day} it is forecasted that there are some places '
                     f'in {loc} that will be {cond}. Interestingly, there '
                     f'would be {fore}',
                     f'Some parts of {loc} will be seeing a bit of {cond} by '
                     f'{day} with average temperature of {feel}. But for the '
                     f'most part it\'ll fluctuate between {max} high & '
                     f'{min} low.',
                     f'Well till {day}, it seems it\'ll be fairly {cond} in '
                     f'some parts of {loc}. Winds can be seen gushing at '
                     f'speeds upto {spd} and as we go through the week the '
                     f'temperature will vary between {max} high & {min} low.']
            _hrs = [f'We are going to see {cond} in the next {hours} hours '
                    f'with {sky} skies in some parts {loc} with temperature '
                    f'fluctuating between {max} high & {min} low.',
                    f'There is going to be {cond} here in {loc} for the next '
                    f'{hours} hours, also we may experience {sky} skies with '
                    f'temperatures spiking upto {temp}.']
            _now = [f'Well, it is {cond} in some places across much of {loc}. '
                    f'Having said that the temperature has been around {temp} '
                    'roughly and will stay the same for the most part of the '
                    f'{part}.',
                    f'It is {cond} in {dir} parts of {loc}. We will however '
                    f'see the temperature between {min} & {max}. '
                    f'Interestingly, there would be {fore}',
                    f'It is {cond} across {dir} {loc} especially in the early '
                    f'hours. It\'s the expected humidity of {hum} with the '
                    'unsettling breeze is affecting the average temperature '
                    f'of {feel}.',
                    f'Looking at {loc} from above, it is {cond}. While some '
                    f'of the areas in {dir} {loc} would get as low as {min} '
                    f'& as high as {max} because of the humidity.',
                    f'Well from above here, it seems it is {cond}. Winds can '
                    f'be seen gushing at speeds upto {spd} across {loc} and '
                    f'as we go throughout the {part} the temperature will'
                    f' vary between {max} high & {min} low.',
                    f'Most likely it is {cond}. However, we could see '
                    f'temperature rise upto {temp} over the grounds of {dir} '
                    f'parts of {loc}. Interestingly, there would be {fore}',
                    f'In the {part} we shall witness {cond} in places across '
                    f'{loc}. It\'s a fine start to the {part} but we\'ve got '
                    'some windy weather which should feel relatively pleasant '
                    f'with the temperature slightly above {temp}.',
                    f'The temperature in {loc} is going to stay between '
                    f'{temp} & {feel} all {part} with a bit of {cond} in the '
                    f'{dir} parts. However, it\'ll be {fore}']

            response = _days if idx == 0 else _hrs if idx == 1 else _now
            shuffle(response)

            return choice(response)
        else:
            # Returns None if no internet connection is available.
            return None
    except Exception as error:
        print('An error occured while performing this operation because of '
              f'{error} in function "{stack()[0][3]}" on line '
              f'{exc_info()[-1].tb_lineno}.')
