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
#   1.1.0 - Reworked `ActionGreetUser` and replaced all weather related classes
#           with `ActionWeatherEvent`.
#           Added internal checks to measuree if the conditions are meeting or
#           not. For e.g: is_charlotte_greeted, is_charlotte_online, etc.
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
from charlotte.utils.actions.weather import weather_event
from charlotte.utils.assists.phrases import (errors,
                                             greetings_protocol,
                                             weather_protocol)
from charlotte.utils.assists.system import check_internet


class ActionGreetUser(Action):
    """Greets user."""

    def name(self) -> str:
        return 'action_greet_user'

    def run(self, dispatcher, tracker, domain) -> list:
        try:
            is_charlotte_greeted = tracker.get_slot('is_charlotte_greeted')
            if is_charlotte_greeted is None:
                response, time, hour, minutes = greet_user()
                dispatcher.utter_message(response)
                return [SlotSet('current_time', time),
                        SlotSet('current_hour', hour),
                        SlotSet('current_minutes', minutes),
                        SlotSet('is_charlotte_greeted', True)]
            else:
                response = choice(greetings_protocol['yes_boss'])
                dispatcher.utter_message(response)
        except Exception as error:
            dispatcher.utter_message(error['unknown'])
            return [SlotSet('current_time', None),
                    SlotSet('current_hour', None),
                    SlotSet('current_minutes', None),
                    SlotSet('is_charlotte_greeted', False)]


class ActionWeatherEvent(Action):
    """Returns weather details."""

    def name(self) -> str:
        return 'action_weather_event'

    def run(self, dispatcher, tracker, domain) -> list:
        try:
            query_city = tracker.get_slot('query_city')
            query_hours = tracker.get_slot('query_hours')
            query_minutes = tracker.get_slot('query_minutes')
            units_imperial = tracker.get_slot('units_imperial')
            is_weather_checked = tracker.get_slot('is_weather_checked')
            is_charlotte_online = tracker.get_slot('is_charlotte_online')
            if units_imperial is not False:
                units_imperial = True
            else:
                units_imperial = False
            if is_charlotte_online is False:
                _retry = True
                _retrying = choice(weather_protocol['retrying'])
                dispatcher.utter_message(_retrying)
            else:
                _retry = False
            if check_internet():
                current_city = locate('city')
                if query_city is None:
                    query_city = current_city
                _query_resp, _query_cond = weather_event(city=query_city,
                                                         hours=query_hours,
                                                         minutes=query_minutes,
                                                         imperial=units_imperial)
                if not is_weather_checked:
                    _working_on_it = choice(weather_protocol['working_on_it'])
                    _saying_okay = choice(weather_protocol['saying_okay'])
                    _choice_resp = choice([_working_on_it, _saying_okay])
                    dispatcher.utter_message(_choice_resp)
                dispatcher.utter_message(_query_resp)
                return [SlotSet('query_city', query_city),
                        SlotSet('query_hours', query_hours),
                        SlotSet('query_minutes', query_minutes),
                        SlotSet('current_city', current_city),
                        SlotSet('query_weather_cond', _query_cond),
                        SlotSet('is_charlotte_online', True),
                        SlotSet('is_weather_checked', True),
                        SlotSet('units_imperial', units_imperial)]
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
                        SlotSet('query_weather_cond', None),
                        SlotSet('is_charlotte_online', False),
                        SlotSet('is_weather_checked', False),
                        SlotSet('units_imperial', False)]
        except Exception as error:
            dispatcher.utter_message(error['unknown'])
            return [SlotSet('query_city', None),
                    SlotSet('query_hours', None),
                    SlotSet('query_minutes', None),
                    SlotSet('current_city', None),
                    SlotSet('query_weather_cond', None),
                    SlotSet('is_charlotte_online', False),
                    SlotSet('is_weather_checked', False),
                    SlotSet('units_imperial', False)]


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
