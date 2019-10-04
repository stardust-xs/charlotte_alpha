## interactive_story_1
* querying_weather_event{"weather_condition": "temperature", "query_city": "Mumbai", "units_imperial": "fahrenheit"}
    - slot{"query_city": "Mumbai"}
    - slot{"units_imperial": "fahrenheit"}
    - action_weather_event
    - slot{"query_city": "Mumbai"}
    - slot{"query_hours": null}
    - slot{"query_minutes": null}
    - slot{"current_city": "Thane"}
    - slot{"query_weather_cond": "Moderate or heavy rain shower"}
    - slot{"is_charlotte_online": true}
    - slot{"is_weather_checked": true}
    - slot{"units_imperial": true}

## interactive_story_2
* querying_weather_event{"weather_condition": "rain", "query_minutes": "10", "time": "minutes"}
    - slot{"query_minutes": "10"}
    - action_weather_event
    - slot{"query_city": "Thane"}
    - slot{"query_hours": null}
    - slot{"query_minutes": "10"}
    - slot{"current_city": "Thane"}
    - slot{"query_weather_cond": "Partly cloudy"}
    - slot{"is_charlotte_online": true}
    - slot{"is_weather_checked": true}
    - slot{"units_imperial": false}
* responding_hello
    - action_greet_user
    - slot{"current_time": "12:08"}
    - slot{"current_hour": 12}
    - slot{"current_minutes": 8}
    - slot{"is_charlotte_greeted": true}
* querying_weather_event{"query_city": "San Fransisco"}
    - slot{"query_city": "San Fransisco"}
    - action_weather_event
    - slot{"query_city": "San Fransisco"}
    - slot{"query_hours": null}
    - slot{"query_minutes": "10"}
    - slot{"current_city": "Thane"}
    - slot{"query_weather_cond": "Partly cloudy"}
    - slot{"is_charlotte_online": true}
    - slot{"is_weather_checked": true}
    - slot{"units_imperial": false}
* responding_thank_you{"hotword": "charlotte"}
    - utter_responding_welcome_to_action
    - utter_do_you_need_anything_else
* responding_no{"xa": "xa"}
    - utter_responding_okay_to_denial
