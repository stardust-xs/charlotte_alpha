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
#   1.0.0 - First code.

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from charlotte.utils.actions.music import (play_music_using_metadata,
                                           play_next_track,
                                           play_previous_track,
                                           reply_on_playing)
from charlotte.utils.actions.person import (wish_user,
                                            locate)
from charlotte.utils.actions.weather import (current_weather,
                                             forecast_weather,
                                             current_forecast_weather)


class ActionGreetUser(Action):
    """Greets user."""

    def name(self) -> str:
        return 'action_greet_user'

    def run(self, dispatcher, tracker, domain) -> list:
        dispatcher.utter_message(wish_user())


class ActionTellCurrentWeatherConditions(Action):
    """Return current weather."""

    def name(self) -> str:
        return 'action_tell_current_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        if city is None:
            city = locate('city')
        dispatcher.utter_message(current_weather(city))
        return [SlotSet('city', city)]


class ActionTellForecastWeatherConditions(Action):
    """Return weather forecast."""

    def name(self) -> str:
        return 'action_tell_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        hours = tracker.get_slot('hours')
        mins = tracker.get_slot('minutes')
        if city is None:
            city = locate('city')
        dispatcher.utter_message(forecast_weather(city, hours, mins))
        return [SlotSet('city', city),
                SlotSet('hours', hours),
                SlotSet('minutes', mins)]


class ActionTellCurrentForecastWeatherConditions(Action):
    """Return weather."""

    def name(self) -> str:
        return 'action_tell_current_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        if city is None:
            city = locate('city')
        dispatcher.utter_message(current_forecast_weather(city))
        return [SlotSet('city', city)]


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
        return [SlotSet('music_file', None),
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
        return [SlotSet('music_file', None),
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
        return [SlotSet('music_file', None),
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
