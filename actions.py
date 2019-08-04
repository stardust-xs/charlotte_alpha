"""
Charlotte Actions
=================

It runs actions.

See https://github.com/xames3/charlotte for complete documentation.
"""
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from charlotte.utils.helpers.actions import (play_music,
                                             current_weather,
                                             forecast_weather,
                                             current_forecast_weather)


class ActionPlayMusicWithTrackName(Action):
    def name(self):
        return 'action_play_music_with_track_name'

    def run(self, dispatcher, tracker, domain) -> list:
        music = tracker.get_slot('track_name')
        dispatcher.utter_message(play_music(music))
        return [SlotSet('track_name', music)]


class ActionPlayAnyMusic(Action):
    def name(self):
        return 'action_play_any_music'

    def run(self, dispatcher, tracker, domain) -> list:
        dispatcher.utter_message(play_music())


class ActionTellCurrentWeatherConditions(Action):
    def name(self):
        return 'action_tell_current_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        dispatcher.utter_message(current_weather(city))
        return [SlotSet('city', city)]


class ActionTellForecaseWeatherConditions(Action):
    def name(self):
        return 'action_tell_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        dispatcher.utter_message(forecast_weather(city))
        return [SlotSet('city', city)]


class ActionTellCurrentForecastWeatherConditions(Action):
    def name(self):
        return 'action_tell_current_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        dispatcher.utter_message(current_forecast_weather(city))
        return [SlotSet('city', city)]
