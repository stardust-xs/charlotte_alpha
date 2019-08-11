"""
Charlotte Action Functions
==========================

This module represents set of actions the Assistant can perform.
The module has 4 functions:
    - age               : Calculates the age
    - locate            : Locates the position of the user
    - find              : Finds the approximate `file name` in a directory
    - play_music        : Plays music from `D:/Music` directory
    - current_weather   : Returns current weather condition
    - forecast_weather  : Returns weather forecast for next 5 hours
    - current_forecast_weather: Returns current weather and forecast

See https://github.com/xames3/charlotte for cloning the repository.
"""
from charlotte.utils.paths.directories import local_dir


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

    try:
        days_in_year = 365.2425
        year = int(birthdate.split('-')[0])
        month = int(birthdate.split('-')[1])
        day = int(birthdate.split('-')[2])
        age = int((date.today() - date(year, month, day)).days / days_in_year)
        return age
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


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
        gmaps = Client(key=os.environ.get('CHARLOTTE_MAPS'))
        current_coords = gmaps.geolocate()
        location = osm(
            list(current_coords['location'].values()), method='reverse')
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
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


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

    try:
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
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def play_music(file: str = None, file_dir: str = local_dir['music']) -> None:
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

    try:
        if file is not None:
            file_name, file_score = find(file, file_dir)
            if file_score == 0:
                return file_name
            else:
                music_file = join(file_dir, file_name)
                startfile(f'{music_file}')
        else:
            random_file = choice([join(local_dir['music'], file) for file in listdir(
                local_dir['music']) if isfile(join(local_dir['music'], file))])
            startfile(random_file)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def current_weather(city: str) -> str:
    """
    Definition
    ----------
        Returns the current weather for provided city.

    Parameter
    ---------
        city : string, mandatory
            Name of the city for which you need to find the weather.

    Returns
    -------
        choice(weather_condition) : string, default
            Current weather conditions for the asked city.

    Notes
    -----
        An account on `https://www.apixu.com` is required to get the api key.
        API calls are made to retreive the weather reports.
    """
    import os
    from random import choice
    from apixu.client import ApixuClient

    try:
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU'))

        local_area = client.current(q=city)
        name = local_area['location']['name']
        condition = local_area['current']['condition']['text']
        temperature_c = local_area['current']['temp_c']
        temperature_f = local_area['current']['temp_f']
        is_day = local_area['current']['is_day']
        wind_kph = local_area['current']['wind_kph']
        wind_mph = local_area['current']['wind_mph']
        wind_degree = local_area['current']['wind_degree']
        wind_dir = local_area['current']['wind_dir']
        pressure_in = local_area['current']['pressure_in']
        pressure_mb = local_area['current']['pressure_mb']
        precip_mm = local_area['current']['precip_mm']
        precip_in = local_area['current']['precip_in']
        humidity = local_area['current']['humidity']
        cloud = local_area['current']['cloud']
        feelslike_c = local_area['current']['feelslike_c']
        feelslike_f = local_area['current']['feelslike_f']
        vis_km = local_area['current']['vis_km']
        vis_miles = local_area['current']['vis_miles']
        uv = local_area['current']['uv']
        gust_kph = local_area['current']['gust_kph']
        gust_mph = local_area['current']['gust_mph']

        day_weather = [f'Currently in {name} it\'s'
                       f' {temperature_c}°C and {condition} with winds'
                       f' running upto {wind_kph} km/h.',
                       f'Right now in {name} it\'s {temperature_c}°C'
                       f' and {condition} but because of the humidity'
                       f' it feels like {feelslike_c}°C.',
                       f'It is currently {condition} in {name} with '
                       f' {temperature_c}°C and winds running upto {wind_kph}'
                       ' km/h.',
                       f'It is {temperature_c}°C and {condition} in {name}'
                       f' with winds running upto {wind_kph} km/h but due to'
                       f' the current humidity it feels like {feelslike_c}°C.',
                       f'Weather in {name} is {temperature_c}°C'
                       f' with {condition} conditions and winds blowing'
                       f' in {wind_dir} direction.',
                       f'The weather today in {name} is {condition}'
                       f' with {temperature_c}°C.']
        night_weather = [f'Tonight the weather is {condition} in {name}'
                         f' with winds blowing in {wind_dir} direction at {wind_kph} km/h. Temperature is {temperature_c}°C.',
                         f'Tonight the weather is {condition} in {name}'
                         f' with {temperature_c}°C but due to {humidity}%'
                         f' humidity it feels like {feelslike_c}°C.',
                         f'The weather tonight in {name} is {condition}'
                         f' with {temperature_c}°C.',
                         f'Right now in {name} it\'s {temperature_c}°C'
                         f' and {condition} but due to humidity'
                         f' it feels like {feelslike_c}°C.',
                         f'Currently in {name} it\'s {temperature_c}°C'
                         f' and {condition} with winds running upto'
                         f' {wind_kph} km/h.']

        if is_day == 0:
            return choice(night_weather)
        else:
            return choice(day_weather)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def forecast_weather(city: str, hours: int = None, mins: int = None) -> str:
    """
    Definition
    ----------
        Returns the weather forecast for provided city.

    Parameter
    ---------
        city : string, mandatory
            Name of the city for which you need to find the forecast.

        hours : integer, optional
            Projected number of hours for which you need weather forecast for.
            Global default: 5 hours

        mins : integer, optional
            Projected number of minutes for which you need weather forecast.
            Global default: 0 mins.

    Returns
    -------
        choice(weather_forecast) : string, default
            Forecasted weather conditions for the asked city.

    Notes
    -----
        An account on `https://www.apixu.com` is required to get the api key.
        API calls are made to retreive the weather reports.
    """
    import os
    from random import choice
    from apixu.client import ApixuClient

    try:
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU'))

        if hours is None or hours is 'None' or hours is 'null':
            if mins is None or mins is 'None' or mins is 'null':
                local_area = client.forecast(q=city, hour=5)
            else:
                min_to_hour = int(mins) // 60
                local_area = client.forecast(q=city, hour=min_to_hour)
        else:
            if int(hours) >= 23:
                local_area = client.forecast(q=city, days=1)
            else:
                local_area = client.forecast(q=city, hour=hours)
        name = local_area['location']['name']
        condition = local_area['current']['condition']['text']
        temperature_c = local_area['current']['temp_c']
        temperature_f = local_area['current']['temp_f']
        is_day = local_area['current']['is_day']
        wind_kph = local_area['current']['wind_kph']
        wind_mph = local_area['current']['wind_mph']
        wind_degree = local_area['current']['wind_degree']
        wind_dir = local_area['current']['wind_dir']
        pressure_in = local_area['current']['pressure_in']
        pressure_mb = local_area['current']['pressure_mb']
        precip_mm = local_area['current']['precip_mm']
        precip_in = local_area['current']['precip_in']
        humidity = local_area['current']['humidity']
        cloud = local_area['current']['cloud']
        feelslike_c = local_area['current']['feelslike_c']
        feelslike_f = local_area['current']['feelslike_f']
        vis_km = local_area['current']['vis_km']
        vis_miles = local_area['current']['vis_miles']
        uv = local_area['current']['uv']
        gust_kph = local_area['current']['gust_kph']
        gust_mph = local_area['current']['gust_mph']
        maxtemp_c = local_area['forecast']['forecastday'][0]['day']['maxtemp_c']
        maxtemp_f = local_area['forecast']['forecastday'][0]['day']['maxtemp_f']
        mintemp_c = local_area['forecast']['forecastday'][0]['day']['mintemp_c']
        mintemp_f = local_area['forecast']['forecastday'][0]['day']['mintemp_f']
        avgtemp_c = local_area['forecast']['forecastday'][0]['day']['avgtemp_c']
        avgtemp_f = local_area['forecast']['forecastday'][0]['day']['avgtemp_f']
        maxwind_kph = local_area['forecast']['forecastday'][0]['day']['maxwind_kph']
        maxwind_mph = local_area['forecast']['forecastday'][0]['day']['maxwind_mph']
        totalprecip_mm = local_area['forecast']['forecastday'][0]['day']['totalprecip_mm']
        totalprecip_in = local_area['forecast']['forecastday'][0]['day']['totalprecip_in']
        avgvis_km = local_area['forecast']['forecastday'][0]['day']['avgvis_km']
        avgvis_miles = local_area['forecast']['forecastday'][0]['day']['avgvis_miles']
        avghumidity = local_area['forecast']['forecastday'][0]['day']['avghumidity']
        forecast_condition = local_area['forecast']['forecastday'][0]['day']['condition']['text']
        forecast_uv = local_area['forecast']['forecastday'][0]['day']['uv']

        day_forecast = [f'Today, it will be {forecast_condition} with maximum'
                        f' temperature of {maxtemp_c}°C and minimum of'
                        f' {mintemp_c}°C.',
                        'The temperature is predicted to be'
                        f' {avgtemp_c}°C and with {forecast_condition}.',
                        f'There will be winds blowing upto {maxwind_kph} km/h'
                        ' and temperature would be anywhere'
                        f' between {maxtemp_c}°C and {mintemp_c}°C.',
                        f'It is forecasted to be about {avgtemp_c}°C with'
                        f' {forecast_condition}.']
        night_forecast = [f'Tonight the weather is predicted to be '
                          f'{forecast_condition} with with maximum'
                          f' temperature of {maxtemp_c}°C and minimum of'
                          f' {mintemp_c}°C.',
                          f'Tonight it is forecasted to be {avgtemp_c}°C with'
                          f' {forecast_condition}.']

        if is_day == 0:
            return choice(night_forecast)
        else:
            return choice(day_forecast)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def current_forecast_weather(city: str) -> str:
    """
    Definition
    ----------
        Returns the weather report for provided city.This inlcudes both
        current weather and weather forecast for that city

    Parameter
    ---------
        city : string, mandatory
            Name of the city for which you need to find the weather.

    Returns
    -------
        choice(weather_current_forecast) : string, default
            Weather conditions and Forecast for the asked city.

    Notes
    -----
        An account on `https://www.apixu.com` is required to get the api key.
        API calls are made to retreive the weather reports.
    """
    return current_weather(city) + ' ' + forecast_weather(city)
