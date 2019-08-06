## play_music_with_genre
* saying_hello
    - utter_saying_hello
* asking_play_any_music_with_genre{"genre": "dubstep"}
    - slot{"genre": "dubstep"}
    - utter_play_any_music_with_genre
    - action_play_any_music
    - slot{"genre": "dubstep"}

## play_any_music
* asking_play_any_music
    - utter_playing_any_music
    - action_play_any_music

## telling_current_forecast_weather_for_home
* asking_current_weather_conditions+asking_forecast_weather_conditions{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_ask_use_home_location_for_weather
* saying_yes
    - utter_saying_fetching_current_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "mumbai"}

## telling_current_forecast_weather_for_asked_city_after_asking_city
* asking_current_weather_conditions+asking_forecast_weather_conditions
    - utter_ask_use_home_location_for_weather
* saying_no
    - utter_saying_okay
    - utter_asking_city_for_weather
* telling_current_location{"city": "chicago"}
    - slot{"city": "chicago"}
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "chicago"}
    - utter_do_you_need_anything_else
* saying_no{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_okay

## telling_current_forecast_weather_for_home_and_asked_city
* asking_current_weather_conditions+asking_forecast_weather_conditions{"date": "today", "ai": "charlotte"}
    - slot{"date": "today"}
    - slot{"ai": "charlotte"}
    - utter_ask_use_home_location_for_weather
* saying_yes
    - utter_saying_fetching_current_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "mumbai"}
    - utter_do_you_need_anything_else
* asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"city": "london"}
    - slot{"city": "london"}
    - utter_saying_okay
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "london"}

## telling_current_forecast_weather_for_asked_city_with_xa_saying_thanks
* asking_current_weather_conditions+asking_forecast_weather_conditions{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_ask_use_home_location_for_weather
* saying_no
    - utter_saying_okay
    - utter_asking_city_for_weather
* telling_current_location{"city": "jaipur"}
    - slot{"city": "jaipur"}
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "jaipur"}
    - utter_do_you_need_anything_else
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_welcome_to_action

## telling_current_forecast_weather_for_mentioned_city
* asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"city": "delhi"}
    - slot{"city": "delhi"}
    - utter_saying_okay
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "delhi"}
    - utter_do_you_need_anything_else
* saying_no

## telling_current_weather_for_home
* asking_current_weather_conditions{"time": "now"}
    - slot{"time": "now"}
    - utter_ask_current_weather_only
* saying_yes
    - utter_ask_use_home_location_for_weather
* saying_okay OR saying_yes
    - utter_saying_fetching_current_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "mumbai"}
    - utter_do_you_need_anything_else
* saying_no{"time": "now"}
    - slot{"time": "now"}
    - utter_saying_okay

## telling_current_forecast_weather_for_asked_city
* asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"time": "now", "city": "alesund"}
    - slot{"city": "alesund"}
    - slot{"time": "now"}
    - utter_saying_okay
    - utter_saying_fetching_current_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "alesund"}
    - utter_do_you_need_anything_else
* saying_no
    - utter_saying_okay

## telling_forecast_weather_for_home
* asking_forecast_weather_conditions
    - utter_ask_forecast_weather_only
* saying_no
    - utter_saying_okay
    - utter_ask_use_home_location_for_weather
* saying_yes
    - utter_saying_fetching_current_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "mumbai"}

## telling_forecast_weather_for_asked_city_with_weather_for_asked_city
* asking_forecast_weather_conditions
    - utter_ask_forecast_weather_only
* saying_no
    - utter_saying_okay
    - utter_ask_use_home_location_for_weather
* telling_current_location{"city": "malibu"}
    - slot{"city": "malibu"}
    - utter_saying_fetching_current_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "malibu"}
    - utter_do_you_need_anything_else
* asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"city": "mumbai"}
    - slot{"city": "mumbai"}
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "mumbai"}
    - utter_do_you_need_anything_else
* saying_no

## telling_weather_for_asked_city_xa_saying_thanks
* asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"ai": "charlotte", "city": "chicago"}
    - slot{"ai": "charlotte"}
    - slot{"city": "chicago"}
    - utter_saying_fetching_current_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "chicago"}
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_welcome_to_action

## telling_forecast_weather_for_asked_city
* asking_forecast_weather_conditions
    - utter_ask_forecast_weather_only
* saying_yes OR saying_okay
    - utter_ask_use_home_location_for_weather
* telling_forecast_location{"city": "london"}
    - slot{"city": "london"}
    - utter_saying_fetching_current_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "london"}
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}

## telling_current_weather_for_asked_city
* asking_current_weather_conditions{"time": "now", "city": "mumbai"}
    - slot{"city": "mumbai"}
    - slot{"time": "now"}
    - utter_ask_current_weather_only
* asking_current_weather_conditions{"time": "now"}
    - slot{"time": "now"}
    - utter_saying_okay
    - utter_saying_fetching_current_weather_details
    - action_tell_current_weather_conditions
    - slot{"city": "mumbai"}
    - utter_do_you_need_anything_else
* saying_no{"ai": "charlotte", "time": "now"}
    - slot{"ai": "charlotte"}
    - slot{"time": "now"}
    - utter_saying_okay

## telling_current_forecast_weather_for_asked_city_and_forecast_again
* saying_hello+asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"city": "rajkot"}
    - slot{"city": "rajkot"}
    - utter_saying_fetching_current_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "rajkot"}
    - utter_do_you_need_anything_else
* asking_forecast_weather_conditions+telling_forecast_location{"city": "rajkot"}
    - slot{"city": "rajkot"}
    - utter_saying_okay
    - utter_saying_fetching_current_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "rajkot"}
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_welcome_to_action

## telling_current_forecast_weather_for_asked_city_and_current_forecast_for_asked_city
* asking_forecast_weather_conditions
    - utter_ask_forecast_weather_only
* asking_forecast_weather_conditions+telling_forecast_location{"city": "aberdeen"}
    - slot{"city": "aberdeen"}
    - utter_saying_fetching_current_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "aberdeen"}
* asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"city": "newcastle"}
    - slot{"city": "newcastle"}
    - utter_saying_okay
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "newcastle"}

## telling_current_weather_for_city
* asking_current_weather_conditions+asking_forecast_weather_conditions+telling_current_location{"city": "houston"}
    - slot{"city": "houston"}
    - utter_saying_okay
    - utter_saying_fetching_current_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "houston"}
