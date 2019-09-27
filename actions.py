"""
The actions module: Runs custom actions.

These classes are run during the inference by the Rasa Custom Actions after
running Action Server. These classes and it`s method are the core actions that
Charlotte executes as per request.

See https://github.com/xames3/charlotte for complete documentation.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.4 - Replaced the exception handling from previous build with if-else
#           conditions.
#   1.0.3 - Added exception handling support when no internet is detected in
#           weather functions.
#   1.0.2 - Slots for music_file in `ActionPlayMusic`, `ActionPlayNextMusic`
#           and `ActionPlayPreviousMusic` are set, previously were kept None.
#   1.0.0 - First code.

from random import choice

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from charlotte.utils.actions.music import (play_music_using_metadata,
                                           play_next_track,
                                           play_previous_track,
                                           reply_on_playing)
from charlotte.utils.actions.person import (greet_user,
                                            locate)
from charlotte.utils.actions.weather import (current_weather,
                                             forecast_weather,
                                             current_forecast_weather)
from charlotte.utils.assists.phrases import (greetings_protocol,
                                             weather_protocol)
from charlotte.utils.assists.system import check_internet


class ActionGreetUser(Action):
    """Greets user."""

    def name(self) -> str:
        return 'action_greet_user'

    def run(self, dispatcher, tracker, domain) -> list:
        is_charlotte_greeted = tracker.get_slot('is_charlotte_greeted')
        if is_charlotte_greeted is False:
            response, time, hour, minutes = greet_user()
            dispatcher.utter_message(response)
            return [SlotSet('current_time', time),
                    SlotSet('current_hour', hour),
                    SlotSet('current_minutes', minutes),
                    SlotSet('is_charlotte_greeted', True)]
        else:
            response = choice(greetings_protocol['yes'])
            dispatcher.utter_message(response)


class ActionTellCurrentWeatherConditions(Action):
    """Returns current weather."""

    def name(self) -> str:
        return 'action_tell_current_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        query_city = tracker.get_slot('query_city')
        is_charlotte_online = tracker.get_slot('is_charlotte_online')
        is_curr_weather_checked = tracker.get_slot('is_curr_weather_checked')
        if is_charlotte_online is False:
            _retry = True
            _retrying = choice(weather_protocol['retrying'])
            dispatcher.utter_message(_retrying)
        else:
            _retry = False
        if check_internet():
            current_city = locate('city')
            current_response, current_weather_cond = current_weather(
                current_city)
            if query_city is None:
                query_weather_cond = None
                response = current_response
            else:
                response, query_weather_cond = current_weather(query_city)
            if not is_curr_weather_checked:
                _working_on_it = choice(weather_protocol['working_on_it'],
                                        weather_protocol['saying_okay'])
                dispatcher.utter_message(_working_on_it)
            dispatcher.utter_message(response)
            return [SlotSet('query_city', query_city),
                    SlotSet('current_city', current_city),
                    SlotSet('query_weather_cond', query_weather_cond),
                    SlotSet('current_weather_cond', current_weather_cond),
                    SlotSet('is_charlotte_online', True),
                    SlotSet('is_curr_weather_checked', True)]
        else:
            if _retry:
                _still_no_internet = choice(
                    weather_protocol['still_no_internet'])
                dispatcher.utter_message(_still_no_internet)
            else:
                _no_internet = choice(weather_protocol['no_internet'])
                dispatcher.utter_message(_no_internet)
            return [SlotSet('query_city', None),
                    SlotSet('current_city', None),
                    SlotSet('query_weather_cond', None),
                    SlotSet('current_weather_cond', None),
                    SlotSet('is_charlotte_online', False)]


class ActionTellForecastWeatherConditions(Action):
    """Returns weather forecast."""

    def name(self) -> str:
        return 'action_tell_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        query_city = tracker.get_slot('query_city')
        query_hours = tracker.get_slot('query_hours')
        query_mins = tracker.get_slot('query_minutes')
        is_charlotte_online = tracker.get_slot('is_charlotte_online')
        if is_charlotte_online is False:
            _retry = True
            _retrying = choice(weather_protocol['retrying'])
            dispatcher.utter_message(_retrying)
        else:
            _retry = False
        if check_internet():
            current_city = locate('city')
            forecast_response, forecast_weather_cond = forecast_weather(
                current_city, query_hours, query_mins)
            if query_city is None:

                query_forecast_cond = None
                response = forecast_response
            else:
                response, query_forecast_cond = forecast_weather(query_city,
                                                                 query_hours,
                                                                 query_mins)
            if not is_fore_weather_checked:
                _working_on_it = choice(weather_protocol['working_on_it'],
                                        weather_protocol['saying_okay'])
                dispatcher.utter_message(_working_on_it)
            dispatcher.utter_message(response)
            return [SlotSet('query_city', query_city),
                    SlotSet('query_hours', query_hours),
                    SlotSet('query_minutes', query_mins),
                    SlotSet('current_city', current_city),
                    SlotSet('query_forecast_cond', query_forecast_cond),
                    SlotSet('forecast_weather_cond', forecast_weather_cond),
                    SlotSet('is_charlotte_online', True)]
        else:
            if _retry:
                _still_no_internet = choice(
                    weather_protocol['still_no_internet'])
                dispatcher.utter_message(_still_no_internet)
            else:
                _no_internet = choice(weather_protocol['no_internet'])
                dispatcher.utter_message(_no_internet)
            return [SlotSet('query_city', None),
                    SlotSet('query_hours', None),
                    SlotSet('query_minutes', None),
                    SlotSet('current_city', None),
                    SlotSet('query_forecast_cond', None),
                    SlotSet('forecast_weather_cond', None),
                    SlotSet('is_charlotte_online', False)]


class ActionTellCurrentForecastWeatherConditions(Action):
    """Returns weather."""

    def name(self) -> str:
        return 'action_tell_current_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        query_city = tracker.get_slot('query_city')
        is_charlotte_online = tracker.get_slot('is_charlotte_online')
        if is_charlotte_online is False:
            _retry = True
            _retrying = choice(weather_protocol['retrying'])
            dispatcher.utter_message(_retrying)
        else:
            _retry = False
        if check_internet():
            current_city = locate('city')
            current_response, current_weather_cond = current_forecast_weather(
                current_city)
            if query_city is None:

                query_weather_cond = None
                response = current_response
            else:
                response, query_weather_cond = current_forecast_weather(
                    query_city)
            if not is_curr_weather_checked:
                _working_on_it = choice(weather_protocol['working_on_it'],
                                        weather_protocol['saying_okay'])
                dispatcher.utter_message(_working_on_it)
            dispatcher.utter_message(response)
            return [SlotSet('query_city', query_city),
                    SlotSet('current_city', current_city),
                    SlotSet('query_weather_cond', query_weather_cond),
                    SlotSet('current_weather_cond', current_weather_cond),
                    SlotSet('is_charlotte_online', True)]
        else:
            if _retry:
                _still_no_internet = choice(
                    weather_protocol['still_no_internet'])
                dispatcher.utter_message(_still_no_internet)
            else:
                _no_internet = choice(weather_protocol['no_internet'])
                dispatcher.utter_message(_no_internet)
            return [SlotSet('query_city', None),
                    SlotSet('current_city', None),
                    SlotSet('query_weather_cond', None),
                    SlotSet('current_weather_cond', None),
                    SlotSet('is_charlotte_online', False)]


class ActionPlayMusic(Action):
    """Plays music."""

    def name(self) -> str:
        return 'action_play_music'

    def run(self, dispatcher, tracker, domain) -> list:
        music_file = tracker.get_slot('music_file')
        track_name = tracker.get_slot('track_name')
        track_artist = tracker.get_slot('track_artist')
        track_albumartist = tracker.get_slot('track_albumartist')
        track_composer = tracker.get_slot('track_composer')
        track_album = tracker.get_slot('track_album')
        track_genre = tracker.get_slot('track_genre')
        track_duration = tracker.get_slot('track_duration')
        track_year = tracker.get_slot('track_year')
        track_filesize = tracker.get_slot('track_filesize')
        playing_file, previous_track, next_track = play_music_using_metadata(
            music_file,
            track_name,
            track_artist,
            track_albumartist,
            track_composer,
            track_album,
            track_genre,
            track_duration,
            track_year,
            track_filesize)
        dispatcher.utter_message(reply_on_playing(playing_file[0],
                                                  playing_file[1],
                                                  playing_file[2]))
        return [SlotSet('music_file', playing_file[0]),
                SlotSet('track_name', None),
                SlotSet('track_artist', None),
                SlotSet('track_albumartist', None),
                SlotSet('track_composer', None),
                SlotSet('track_album', None),
                SlotSet('track_genre', None),
                SlotSet('track_duration', None),
                SlotSet('track_year', None),
                SlotSet('track_filesize', None),
                SlotSet('previous_track', previous_track),
                SlotSet('next_track', next_track)]


class ActionPlayPreviousMusic(Action):
    """Plays previous track."""

    def name(self) -> str:
        return 'action_play_previous_music'

    def run(self, dispatcher, tracker, domain) -> list:
        previous_music_file = tracker.get_slot('previous_track')
        playing_file, previous_track, next_track = play_previous_track(
            previous_track=previous_music_file)
        dispatcher.utter_message(reply_on_playing(playing_file[0],
                                                  playing_file[1],
                                                  playing_file[2]))
        return [SlotSet('music_file', playing_file[0]),
                SlotSet('track_name', None),
                SlotSet('track_artist', None),
                SlotSet('track_albumartist', None),
                SlotSet('track_composer', None),
                SlotSet('track_album', None),
                SlotSet('track_genre', None),
                SlotSet('track_duration', None),
                SlotSet('track_year', None),
                SlotSet('track_filesize', None),
                SlotSet('previous_track', previous_track),
                SlotSet('next_track', next_track)]


class ActionPlayNextMusic(Action):
    """Plays next track."""

    def name(self) -> str:
        return 'action_play_next_music'

    def run(self, dispatcher, tracker, domain) -> list:
        next_music_file = tracker.get_slot('next_track')
        playing_file, previous_track, next_track = play_next_track(
            next_track=next_music_file)
        dispatcher.utter_message(reply_on_playing(playing_file[0],
                                                  playing_file[1],
                                                  playing_file[2]))
        return [SlotSet('music_file', playing_file[0]),
                SlotSet('track_name', None),
                SlotSet('track_artist', None),
                SlotSet('track_albumartist', None),
                SlotSet('track_composer', None),
                SlotSet('track_album', None),
                SlotSet('track_genre', None),
                SlotSet('track_duration', None),
                SlotSet('track_year', None),
                SlotSet('track_filesize', None),
                SlotSet('previous_track', previous_track),
                SlotSet('next_track', next_track)]
