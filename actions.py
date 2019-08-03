"""
Charlotte Actions
=================

It runs actions.

See https://github.com/xames3/charlotte for complete documentation.
"""
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from charlotte.utils.helpers.actions import play_music


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


class ActionTellWeatherConditions(Action):
    def name(self):
        return 'action_tell_weather_condition'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        dispatcher.utter_message(print(city))
        return [SlotSet('city', city)]
