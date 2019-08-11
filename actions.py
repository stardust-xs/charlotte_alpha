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


class ActionTellCurrentWeatherConditions(Action):
    def name(self):
        return 'action_tell_current_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        if city is None:
            city = tracker.get_slot('xa_home_city')
        dispatcher.utter_message(current_weather(city))
        return [SlotSet('city', city)]


class ActionTellForecastWeatherConditions(Action):
    def name(self):
        return 'action_tell_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        hours = tracker.get_slot('hours')
        mins = tracker.get_slot('minutes')
        if city is None:
            city = tracker.get_slot('xa_home_city')
        dispatcher.utter_message(forecast_weather(city, hours, mins))
        return [SlotSet('city', city),
                SlotSet('hours', hours),
                SlotSet('minutes', mins)]


class ActionTellCurrentForecastWeatherConditions(Action):
    def name(self):
        return 'action_tell_current_forecast_weather_conditions'

    def run(self, dispatcher, tracker, domain) -> list:
        city = tracker.get_slot('city')
        if city is None:
            city = tracker.get_slot('xa_home_city')
        dispatcher.utter_message(current_forecast_weather(city))
        return [SlotSet('city', city)]
