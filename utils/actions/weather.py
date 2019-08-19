"""
This module packs set of functions related to weather search and forecast.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info


def current_weather(city: str) -> str:
    """
    Definition
    ----------
        Returns the current weather for provided city.

    Parameter
    ---------
        city : string, mandatory
            Name of the city for which you need to find the current weather.

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
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU_KEY'))

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

        at_am = [f'Currently in {name} it\'s {temperature_c}°C and'
                 f' {condition} with winds running upto {wind_kph} km/h.',
                 f'Right now in {name} it\'s {temperature_c}°C and {condition}'
                 f' but because of the humidity it feels like'
                 f' {feelslike_c}°C.',
                 f'It is currently {condition} in {name} with '
                 f' {temperature_c}°C and winds running upto {wind_kph} km/h.',
                 f'It is {temperature_c}°C and {condition} in {name}'
                 f' with winds running upto {wind_kph} km/h but due to'
                 f' the current humidity it feels like {feelslike_c}°C.',
                 f'Weather in {name} is {temperature_c}°C with {condition}'
                 f' conditions and winds blowing in {wind_dir} direction.',
                 f'The weather today in {name} is {condition} with'
                 f' {temperature_c}°C.']
        at_pm = [f'Tonight the weather is {condition} in {name} with winds'
                 f' blowing in {wind_dir} direction at {wind_kph} km/h.'
                 f' Temperature is {temperature_c}°C.',
                 f'Tonight the weather is {condition} in {name} with'
                 f' {temperature_c}°C but due to {humidity}% humidity it feels'
                 f' like {feelslike_c}°C.',
                 f'The weather tonight in {name} is {condition} with'
                 f' {temperature_c}°C.',
                 f'Right now in {name} it\'s {temperature_c}°C and {condition}'
                 f' but due to humidity it feels like {feelslike_c}°C.',
                 f'Currently in {name} it\'s {temperature_c}°C and {condition}'
                 f' with winds running upto {wind_kph} km/h.']

        if is_day == 0:
            return choice(at_pm)
        else:
            return choice(at_am)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


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
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU_KEY'))

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

        at_am = [f'Today, it will be {forecast_condition} with maximum'
                 f' temperature of {maxtemp_c}°C and minimum of'
                 f' {mintemp_c}°C.',
                 f'The temperature in {name} is predicted to be {avgtemp_c}°C'
                 f' and with {forecast_condition}.',
                 f'There will be winds blowing upto {maxwind_kph} km/h and'
                 f' temperature would be anywhere between {maxtemp_c}°C and'
                 f' {mintemp_c}°C.',
                 f'It is forecasted to be about {avgtemp_c}°C with'
                 f' {forecast_condition} in {name}.']
        at_pm = [f'Tonight, the weather in {name} is predicted to be'
                 f' {forecast_condition} with maximum temperature of'
                 f' {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                 f'Well, tonight it is forecasted to be {avgtemp_c}°C with'
                 f' {forecast_condition} in {name}.']
        with_hrs = [f'Well, the weather for {name} in next {hours} hours is'
                    f' forecasted to be {forecast_condition} with maximum'
                    f' of {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                    f'The climate for {name} in next {hours} hours is'
                    f' predicted to be {avgtemp_c}°C and with'
                    f' {forecast_condition}.',
                    f'In {name}, is forecasted to be about {avgtemp_c}°C with'
                    f' {forecast_condition} in next {hours} hours.']
        with_mins = [f'Well, the weather for {name} in next {mins} mins is'
                     f' forecasted to be {forecast_condition} with maximum'
                     f' of {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                     f'The climate for {name} in next {mins} mins is'
                     f' predicted to be {avgtemp_c}°C and with'
                     f' {forecast_condition}.',
                     f'In {name}, is forecasted to be about {avgtemp_c}°C with'
                     f' {forecast_condition} in next {mins} mins.']

        if hours is None or hours is 'None' or hours is 'null':
            if mins is None or mins is 'None' or mins is 'null':
                if is_day == 0:
                    return choice(at_pm)
                else:
                    return choice(at_am)
            else:
                return choice(with_mins)
        else:
            return choice(with_hrs)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def current_forecast_weather(city: str) -> str:
    """
    Definition
    ----------
        Returns the weather report for provided city. This inlcudes both
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
