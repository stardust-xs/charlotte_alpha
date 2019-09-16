"""
The weather module: Provides functions related to weather search and forecast.

These functions help you to perform weather related queries with relative ease.

At a glance, the structure of the module is following:
 - current_weather():   Returns current weather. This is done using API call to
                        the APIXU database.
 - forecast_weather():  Returns weather forecast. It can return weather
                        forecast on basis of hours or minutes. This is done
                        too using API call to the APIXU database.
 - current_forecast_weather(): Returns both current weather and the forecast.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.3 - All the functions returns None if any error or exception is raised.
#   1.0.2 - Fixed error caused by redundant quotes in `forecast_weather`
#           function.
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info

# Constant used by `forecast_weather` to pass None.
_NONE = 'None'
# Constant used by `forecast_weather` to pass null.
_NULL = 'null'


def current_weather(city: str) -> str:
    """Returns current weather.

    city: Name of the city for which you need to find the current weather.

    Returns current weather. This is done using API call to the APIXU database.

    Note: An account on `https://www.apixu.com` is required to get the api key.
    API calls are made to retreive the weather reports.

    Caution: If you run the function without passing valid API key, it will
    raise an exception.
    """
    import os
    from random import choice
    from apixu.client import ApixuClient

    try:
        # Passing the Apixu API key.
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU_KEY'))
        # Locating the city and hitting it with query. The response returned
        # is a JSON response.
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
        # Responses for day time.
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
        # Responses for night time.
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
        # Checks if it is day using the Apixu`s internal sunset time checker.
        if is_day == 0:
            return choice(at_pm)
        else:
            return choice(at_am)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
        return None


def forecast_weather(city: str, hours: int = None, mins: int = None) -> str:
    """Returns weather forecast.

    city:  Name of the city for which you need to find the forecast.
    hours: Projected number of hours for which you need weather forecast for.
           Default: 5 hours
    mins:  Projected number of minutes for which you need weather forecast.
           Default: 0 mins.

    Returns weather forecast. It can return weather forecast on basis of hours
    or minutes. This is done using API call to the APIXU database.

    Note: An account on `https://www.apixu.com` is required to get the api key.
    API calls are made to retreive the weather reports.

    Caution: If you run the function without passing valid API key, it will
    raise an exception.
    """
    import os
    from random import choice
    from apixu.client import ApixuClient

    try:
        # Passing the Apixu API key.
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU_KEY'))
        # Locating the city and hitting it with query basis on the time units
        # passed. The response returned is a JSON response.
        if hours is None or hours is _NONE or hours is _NULL:
            if mins is None or mins is _NONE or mins is _NULL:
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
        # Responses for day time.
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
        # Responses for night time.
        at_pm = [f'Tonight, the weather in {name} is predicted to be'
                 f' {forecast_condition} with maximum temperature of'
                 f' {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                 f'Well, tonight it is forecasted to be {avgtemp_c}°C with'
                 f' {forecast_condition} in {name}.']
        # Responses for hourly forecast.
        with_hrs = [f'Well, the weather for {name} in next {hours} hours is'
                    f' forecasted to be {forecast_condition} with maximum'
                    f' of {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                    f'The climate for {name} in next {hours} hours is'
                    f' predicted to be {avgtemp_c}°C and with'
                    f' {forecast_condition}.',
                    f'In {name}, is forecasted to be about {avgtemp_c}°C with'
                    f' {forecast_condition} in next {hours} hours.']
        # Responses for forecast based on minutes.
        with_mins = [f'Well, the weather for {name} in next {mins} mins is'
                     f' forecasted to be {forecast_condition} with maximum'
                     f' of {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                     f'The climate for {name} in next {mins} mins is'
                     f' predicted to be {avgtemp_c}°C and with'
                     f' {forecast_condition}.',
                     f'In {name}, is forecasted to be about {avgtemp_c}°C with'
                     f' {forecast_condition} in next {mins} mins.']
        # Checks if hours or minutes are passed for predicting the weather.
        if hours is None or hours is _NONE or hours is _NULL:
            if mins is None or mins is _NONE or mins is _NULL:
                # Checks if it is day using the Apixu`s internal sunset time
                # checker.
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
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
        return None


def current_forecast_weather(city: str) -> str:
    """Returns weather.

    city: Name of the city for which you need to find the weather.

    This is combination of both the `current_weather` and `forecast_weather`
    functions.
    """
    try:
        return current_weather(city) + ' ' + forecast_weather(city)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
        return None
