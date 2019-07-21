"""
Charlotte`s actions
===================

It runs actions.

See https://github.com/xames3/charlotte for complete documentation.
"""
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from utils.functions.assistant import play_music


class ActionPlayMusicWithTrackName(Action):
    def name(self):
        return 'action_play_music_with_track_name'

    def run(self, dispatcher, tracker, domain: dict) -> list:
        music = tracker.get_slot('track_name')
        dispatcher.utter_message(play_music(music))
        return [SlotSet('track_name', music)]


class ActionPlayAnyMusic(Action):
    def name(self):
        return 'action_play_any_music'

    def run(self, dispatcher, tracker, domain: dict) -> list:
        dispatcher.utter_message(play_music())
