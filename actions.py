"""
Charlotte Actions
=================

It runs actions.

See https://github.com/xames3/charlotte for complete documentation.
"""
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from charlotte.utils.actions.music import play_music_by_attribute
from charlotte.utils.actions.person import wish_user, locate
from charlotte.utils.actions.weather import (current_weather,
                                             forecast_weather,
                                             current_forecast_weather)


class ActionGreetUser(Action):
    def name(self) -> str:
        return 'action_greet_user'

    def run(self, dispatcher, tracker, domain) -> list:
        dispatcher.utter_message(wish_user())


class ActionTellCurrentWeatherConditions(Action):
    def name(self) -> str:
        return 'action_tell_current_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        if city is None:
            city = locate('city')
        dispatcher.utter_message(current_weather(city))
        return [SlotSet('city', city)]


class ActionTellForecastWeatherConditions(Action):
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
    def name(self) -> str:
        return 'action_tell_current_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        if city is None:
            city = locate('city')
        dispatcher.utter_message(current_forecast_weather(city))
        return [SlotSet('city', city)]


class ActionPlayMusic(Action):
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

        playing_file = play_music_by_attribute(music_file,
                                               track_name,
                                               track_artist,
                                               track_albumartist,
                                               track_composer,
                                               track_album,
                                               track_genre,
                                               track_duration,
                                               track_year,
                                               track_filesize)

        return [SlotSet('music_file', music_file),
                SlotSet('track_name', playing_file),
                SlotSet('track_artist', track_artist),
                SlotSet('track_albumartist', track_albumartist),
                SlotSet('track_composer', track_composer),
                SlotSet('track_album', track_album),
                SlotSet('track_genre', track_genre),
                SlotSet('track_duration', track_duration),
                SlotSet('track_year', track_year),
                SlotSet('track_filesize', track_filesize)]
