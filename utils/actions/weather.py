"""
The weather module: Provides functions related to weather search and forecast.

These functions help you to perform weather related queries with relative ease.

At a glance, the structure of the module is following:
 - _current():          Returns current weather. This is done using API call to
                        the APIXU database. An account on
                        `https://www.apixu.com` is required to get the api key.
                        API calls are made to retreive the weather reports.
                        If you run the function without passing valid API key,
                        it will raise an exception.
 - _predict():          Returns weather forecast. It can return weather
                        forecast on basis of hours or minutes. This is done
                        too using API call to the APIXU database.
 - weather_event():     Returns both current weather and the forecast.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.0 - Added new constants for supporting weather retreival in Imperial
#           metric system.
#           `_current` and `_predict` now replaces previous functions for
#           better support and integration.
#           `weather_event` now replaces `current_forecast_weather` function.
#           `_predict()` now has more natural responses for weather
#           predictions.
#   1.0.7 - Fixed typo in `current_weather` function.
#   1.0.6 - All the functions now return None if internet is not available.
#   1.0.4 - `current_weather` and `forecast_weather` function now uses
#           `check_internet` to check if internet connection is available.
#           'current_forecast_weather' now also retuns None if no internet is
#           detected.
#           Added internal comments while returning None in all functions.
#   1.0.3 - All the functions returns None if any error or exception is raised.
#   1.0.2 - Fixed error caused by redundant quotes in `forecast_weather`
#           function.
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info

from charlotte.utils.assists.system import check_internet

# Constant used by `forecast_weather` to pass None.
_NONE = 'None'
# Constant used by `forecast_weather` to pass null.
_NULL = 'null'
# Constant used for denoting celcius.
_CELCIUS = '°C'
# Constant used for denoting fahrenheit.
_FAHRENHEIT = '°F'
# Constant used for denoting kph.
_KPH = 'km/h'
# Constant used for denoting mph.
_MPH = 'mph'


def _current(city: str, imperial: bool = False) -> str:
    """Returns current weather.

    city:     Name of the city to query the weather details for.
    imperial: Boolean choice to choose between metric or imperial system.
              Default: False.

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
        if check_internet():
            # Passing the Apixu API key.
            client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU_KEY'))
            # Locating the city and hitting it with query. The response
            # returned is a JSON response.
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
            if imperial is False:
                temperature = temperature_c
                degree = _CELCIUS
                wind = wind_kph
                speed = _KPH
                pressure = pressure_mb
                precip = precip_mm
                feelslike = feelslike_c
                vis = vis_km
                gust = gust_kph
            else:
                temperature = temperature_f
                degree = _FAHRENHEIT
                wind = wind_mph
                speed = _MPH
                pressure = pressure_in
                precip = precip_in
                feelslike = feelslike_f
                vis = vis_miles
                gust = gust_mph
            # Responses for day time.
            at_am = [f'Currently in {name} it\'s {temperature}{degree} and'
                     f' {condition} with winds running upto {wind} {speed}.',
                     f'Right now in {name} it\'s {temperature}{degree} and'
                     f' {condition}'
                     f' but because of the humidity it feels like'
                     f' {feelslike}{degree}.',
                     f'It is currently {condition} in {name} with'
                     f' {temperature}{degree} and winds running upto {wind}'
                     f' {speed}.',
                     f'It is {temperature}{degree} and {condition} in {name}'
                     f' with winds running upto {wind} {speed} but due to'
                     f' the current humidity it feels like'
                     f' {feelslike}{degree}.',
                     f'Weather in {name} is {temperature}{degree} with'
                     f' {condition} conditions and winds blowing in {wind_dir}'
                     ' direction.',
                     f'The weather today in {name} is {condition} with'
                     f' {temperature}{degree}.']
            # Responses for night time.
            at_pm = [f'Tonight the weather is {condition} in {name} with winds'
                     f' blowing in {wind_dir} direction at {wind} {speed}.'
                     f' Temperature is {temperature}{degree}.',
                     f'Tonight the weather is {condition} in {name} with'
                     f' {temperature}{degree} but due to {humidity}% humidity'
                     f' it feels like {feelslike}{degree}.',
                     f'The weather tonight in {name} is {condition} with'
                     f' {temperature}{degree}.',
                     f'Right now in {name} it\'s {temperature}{degree} and'
                     f' {condition} but due to humidity it feels like'
                     f' {feelslike}{degree}.',
                     f'Currently in {name} it\'s {temperature}{degree} and'
                     f' {condition} with winds running upto {wind} {speed}.']
            # Checks if it is day using Apixu`s internal sunset time checker.
            if is_day == 0:
                return choice(at_pm), condition
            else:
                return choice(at_am), condition
        else:
            # Returns None if no internet connection is available.
            return None, None
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def _predict(city: str,
             hours: int = None,
             minutes: int = None,
             imperial: bool = False) -> str:
    """Returns weather forecast.

    city:     Name of the city to query the weather details for.
    hours:    Projected  hours for which you need weather forecast for.
              Default: 5 hours
    minutes:  Projected minutes for which you need weather forecast for.
              Default: 0 minutes.
    imperial: Boolean choice to choose between metric or imperial system.
              Default: False.

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
        if check_internet():
            # Passing the Apixu API key.
            client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU_KEY'))
            # Locating the city and hitting it with query basis on the time
            # units passed. The response returned is a JSON response.
            if hours is None or hours is _NONE or hours is _NULL:
                if minutes is None or minutes is _NONE or minutes is _NULL:
                    local_area = client.forecast(q=city, hour=5)
                else:
                    min_to_hour = int(minutes) // 60
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
            if imperial is False:
                temperature = temperature_c
                degree = _CELCIUS
                wind = wind_kph
                speed = _KPH
                pressure = pressure_mb
                precip = precip_mm
                feelslike = feelslike_c
                vis = vis_km
                gust = gust_kph
                maxtemp = maxtemp_c
                mintemp = mintemp_c
                avgtemp = avgtemp_c
                maxwind = maxwind_kph
                totalprecip = totalprecip_mm
                avgvis = avgvis_km
            else:
                temperature = temperature_f
                degree = _FAHRENHEIT
                wind = wind_mph
                speed = _MPH
                pressure = pressure_in
                precip = precip_in
                feelslike = feelslike_f
                vis = vis_miles
                gust = gust_mph
                maxtemp = maxtemp_f
                mintemp = mintemp_f
                avgtemp = avgtemp_f
                maxwind = maxwind_mph
                totalprecip = totalprecip_in
                avgvis = avgvis_miles
            # Responses for day time.
            at_am = [f'Later today, it will be {forecast_condition} with'
                     f' maximum temperature of {maxtemp}{degree}'
                     f' and minimum of {mintemp}{degree}.',
                     'Later the temperature is predicted to be'
                     f' {avgtemp}{degree} and with {forecast_condition}.',
                     f'There will be winds blowing upto {maxwind} {speed} and'
                     ' temperature would be anywhere between'
                     f' {maxtemp}{degree} and {mintemp}{degree}.',
                     f'It is forecasted to be about {avgtemp}{degree} with'
                     f' {forecast_condition}.']
            # Responses for night time.
            at_pm = ['Later tonight, the weather is predicted to be'
                     f' {forecast_condition} with maximum temperature of'
                     f' {maxtemp}{degree} and minimum of {mintemp}{degree}.',
                     f'Also, tonight it is forecasted to be {avgtemp}{degree}'
                     f' with {forecast_condition}.']
            # Responses for hourly forecast.
            with_hrs = [f'Speaking of forecast, the weather in next {hours}'
                        f' hours is forecasted to be {forecast_condition} with'
                        f' maximum of {maxtemp}{degree} and minimum of'
                        f' {mintemp}{degree}.',
                        f'In next {hours} hours it is predicted to be'
                        f' {avgtemp}{degree} and with {forecast_condition}.',
                        f'Well here it is forecasted to be about'
                        f' {avgtemp}{degree} with {forecast_condition} in'
                        f' next {hours} hours.']
            # Responses for forecast based on minutes.
            with_minutes = [f'Well in next {minutes} minutes, it is forecasted'
                            f' to be {forecast_condition} with maximum of'
                            f' {maxtemp}{degree} and minimum of'
                            f' {mintemp}{degree}.',
                            'Speaking of forecast, the weather in next'
                            f' {minutes} minutes is predicted to be'
                            f' {avgtemp}{degree} and with'
                            f' {forecast_condition}.',
                            'Well, it is forecasted to be about'
                            f' {avgtemp}{degree} with {forecast_condition}'
                            f' in next {minutes} minutes.']
            # Checks if hours or minutes are passed for predicting the weather.
            if hours is None or hours is _NONE or hours is _NULL:
                if minutes is None or minutes is _NONE or minutes is _NULL:
                    # Checks if it is day using the Apixu`s internal sunset time
                    # checker.
                    if is_day == 0:
                        return choice(at_pm), condition
                    else:
                        return choice(at_am), condition
                else:
                    return choice(with_minutes), condition
            else:
                return choice(with_hrs), condition
        else:
            # Returns None if no internet connection is available.
            return None, None
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def weather_event(city: str,
                  current: bool = None,
                  hours: int = None,
                  minutes: int = None,
                  imperial: bool = False) -> str:
    """Returns weather details.

    city:     Name of the city to query the weather details for.
    current:  Boolean choice to choose between current or prediction.
              Default: None
    hours:    Projected  hours for which you need weather forecast for.
              Default: 5 hours
    minutes:  Projected minutes for which you need weather forecast for.
              Default: 0 minutes.
    imperial: Boolean choice to choose between metric or imperial system.
              Default: False.

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
        if check_internet():
            _curr_value, _curr_cond = _current(city, imperial)
            _pred_value, _pred_cond = _predict(city, hours, minutes, imperial)
            if current is True:
                return _curr_value, _curr_cond
            elif current is False:
                return _pred_value, _pred_cond
            else:
                return _curr_value + ' ' + _pred_value, _curr_cond
        else:
            # Returns None if any exception was raised or if internet is not
            # available.
            return None, None
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
