"""
Charlotte`s actions
===================

It runs actions.

See https://github.com/xames3/charlotte for complete documentation.
"""
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from utils.functions.assistant import play_music
from utils.profile.user import ai_lower, ai_title, lower, title


class ActionPlayMusic(Action):
    def name(self):
        return 'action_playing_music'

    def run(self, dispatcher, tracker, domain: dict) -> list:

        music = tracker.get_slot('track_name')
        dispatcher.utter_message(play_music(music))
        return [SlotSet('track_name', music)]
