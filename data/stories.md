## 1_telling_current_weather_for_current_city
* asking_current_weather_conditions{"time": "now"}
    - slot{"time": "now"}
    - utter_saying_okay_for_weather_searches
    - action_tell_current_weather_conditions
    - slot{"city": "Mumbai"}

## 2_telling_weather_forecast_for_current_city
* asking_forecast_weather_conditions
    - utter_saying_okay_for_weather_searches
    - action_tell_forecast_weather_conditions
    - slot{"city": "Mumbai"}
    - slot{"hours": null}
    - slot{"minutes": null}

## 3_telling_current_weather_for_mentioned_city
* asking_current_weather_conditions{"time": "now", "city": "allen"}
    - slot{"city": "allen"}
    - slot{"time": "now"}
    - utter_saying_fetching_weather_details
    - action_tell_current_weather_conditions
    - slot{"city": "allen"}

## 4_telling_weather_forecast_for_mentioned_city
* asking_forecast_weather_conditions{"forecast": "forecast", "city": "berlin"}
    - slot{"city": "berlin"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "berlin"}
    - slot{"hours": null}
    - slot{"minutes": null}

## 5_telling_weather_for_current_city
* asking_weather_conditions
    - utter_saying_okay_for_weather_searches
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "Mumbai"}

## 6_telling_weather_for_mentioned_city
* asking_weather_conditions{"city": "lyon"}
    - slot{"city": "lyon"}
    - utter_saying_fetching_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "lyon"}

## 7_telling_weather_forecast_for_current_city_in_xx_hours
* asking_forecast_weather_conditions{"hours": "6"}
    - slot{"hours": "6"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "Mumbai"}
    - slot{"hours": "6"}
    - slot{"minutes": null}

## 8_telling_weather_forecast_for_current_city_in_xx_mins
* asking_forecast_weather_conditions{"minutes": "15"}
    - slot{"minutes": "15"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "Mumbai"}
    - slot{"hours": null}
    - slot{"minutes": "15"}

## 9_telling_weather_forecast_for_mentioned_city_in_xx_hours
* asking_forecast_weather_conditions{"hours": "23", "city": "montreal"}
    - slot{"city": "montreal"}
    - slot{"hours": "23"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "montreal"}
    - slot{"hours": "23"}
    - slot{"minutes": null}

## 10_telling_weather_forecast_for_mentioned_city_in_xx_mins
* asking_forecast_weather_conditions{"city": "tokyo", "minutes": "57", "time": "minutes"}
    - slot{"city": "tokyo"}
    - slot{"minutes": "57"}
    - slot{"time": "minutes"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "tokyo"}
    - slot{"hours": null}
    - slot{"minutes": "57"}

## 11_telling_weather_for_current_city_with_user_saying_thanks
* asking_weather_conditions{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_okay_for_weather_searches
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "Mumbai"}
* saying_thank_you
    - utter_saying_welcome_to_action
    - utter_do_you_need_anything_else
* saying_no
    - utter_saying_okay_to_denial

## 12_telling_current_weather_for_current_and_mentioned_city
* saying_hello
    - action_greet_user
    - utter_how_can_i_help
* asking_current_weather_conditions{"time": "now"}
    - slot{"time": "now"}
    - utter_saying_okay_for_weather_searches
    - action_tell_current_weather_conditions
    - slot{"city": "Mumbai"}
* asking_current_weather_conditions{"city": "moscow", "time": "right now"}
    - slot{"city": "moscow"}
    - slot{"time": "right now"}
    - utter_saying_fetching_weather_details
    - action_tell_current_weather_conditions
    - slot{"city": "moscow"}
    - utter_do_you_need_anything_else
* saying_no
    - utter_saying_okay_to_denial

## 13_telling_weather_forecast_for_current_city_with_user_saying_thanks
* saying_hello
    - action_greet_user
    - utter_how_can_i_help
* asking_forecast_weather_conditions{"minutes": "10", "time": "minutes"}
    - slot{"minutes": "10"}
    - slot{"time": "minutes"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "Mumbai"}
    - slot{"hours": null}
    - slot{"minutes": "10"}
* saying_thank_you
    - utter_saying_welcome_to_action

## 14_wishing_user_and_telling_weather_for_current_city
* saying_hello{"time": "morning"}
    - slot{"time": "morning"}
    - action_greet_user
    - utter_how_can_i_help
* asking_weather_conditions
    - utter_saying_okay_for_weather_searches
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "Mumbai"}
* saying_thank_you
    - utter_saying_welcome_to_action
    - utter_do_you_need_anything_else
* saying_no
    - utter_saying_okay_to_denial

## 15_wishing_user_telling_forecast_for_mentioned_city_saying_thanks_saying_yes_for_request_requesting_weather_for_mentioned_city
* saying_hello{"time": "morning", "ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - slot{"time": "morning"}
    - action_greet_user
    - utter_how_can_i_help
* asking_forecast_weather_conditions{"city": "paris", "hours": "3"}
    - slot{"city": "paris"}
    - slot{"hours": "3"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "paris"}
    - slot{"hours": "3"}
    - slot{"minutes": null}
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_welcome_to_action
    - utter_do_you_need_anything_else
* saying_yes
    - utter_saying_what_would_that_be
* asking_weather_conditions{"city": "munich"}
    - slot{"city": "munich"}
    - utter_saying_fetching_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "munich"}
    - utter_do_you_need_anything_else
* saying_thank_you
    - utter_saying_welcome_to_action

## 16_saying_hello_and_telling_current_weather_for_mentioned_city
* saying_hello
    - action_greet_user
    - utter_how_can_i_help
* asking_current_weather_conditions{"city": "vienna", "time": "right now"}
    - slot{"city": "vienna"}
    - slot{"time": "right now"}
    - utter_saying_fetching_weather_details
    - action_tell_current_weather_conditions
    - slot{"city": "vienna"}

## 17_saying_hello_telling_weather_pulling_wrong_weather_asking_again
* saying_hello
    - action_greet_user
    - utter_how_can_i_help
* asking_weather_conditions{"city": "brooklyn"}
    - slot{"city": "brooklyn"}
    - utter_saying_fetching_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "brooklyn"}
* saying_thank_you
    - utter_saying_welcome_to_action
    - utter_do_you_need_anything_else
* saying_yes
    - utter_saying_what_would_that_be
* asking_forecast_weather_conditions{"minutes": "25", "time": "minutes"}
    - slot{"minutes": "25"}
    - slot{"time": "minutes"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "brooklyn"}
    - slot{"hours": null}
    - slot{"minutes": "25"}
* asking_forecast_weather_conditions{"city": "mumbai", "minutes": "25"}
    - slot{"city": "mumbai"}
    - slot{"minutes": "25"}
    - utter_saying_okay_for_weather_searches
    - action_tell_forecast_weather_conditions
    - slot{"city": "mumbai"}
    - slot{"hours": null}
    - slot{"minutes": "25"}
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_welcome_to_action

## 18_saying_hello_and_then_nothing
* saying_hello{"gender": "female"}
    - slot{"gender": "female"}
    - action_greet_user
    - utter_how_can_i_help

## 19_asking_weather_forecast_weather_for_different_cities
* asking_weather_conditions{"city": "alice"}
    - slot{"city": "alice"}
    - utter_saying_fetching_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "alice"}
* saying_okay
    - utter_do_you_need_anything_else
    - utter_do_you_need_anything_else
* saying_yes
    - utter_saying_what_would_that_be
* asking_forecast_weather_conditions{"city": "mumbai"}
    - slot{"city": "mumbai"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "mumbai"}
    - slot{"hours": null}
    - slot{"minutes": null}
    - utter_do_you_need_anything_else
* asking_weather_conditions{"city": "birmingham"}
    - slot{"city": "birmingham"}
    - utter_saying_fetching_weather_details
    - action_tell_current_forecast_weather_conditions
    - slot{"city": "birmingham"}
    - utter_do_you_need_anything_else
* saying_no
    - utter_saying_okay_to_denial

## 20_saying_hello_asking_forecast_for_mentioned_city_and_saying_thanks
* saying_hello
    - action_greet_user
    - utter_how_can_i_help
* asking_forecast_weather_conditions{"city": "london", "minutes": "56", "time": "minutes"}
    - slot{"city": "london"}
    - slot{"minutes": "56"}
    - slot{"time": "minutes"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "london"}
    - slot{"hours": null}
    - slot{"minutes": "56"}
* saying_thank_you
    - utter_saying_welcome_to_action

## 21_saying_hello_asking_for_nothing
* saying_hello{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - action_greet_user
    - utter_how_can_i_help
* saying_no
    - utter_saying_okay_to_denial

## 22_playing_music_with_track_name_and_artist
* asking_play_music{"track_name": "berserk", "track_artist": "eminem"}
    - slot{"track_artist": "eminem"}
    - slot{"track_name": "berserk"}
    - action_play_music
    - slot{"music_file": "15 - Berzerk.mp3"}
    - slot{"track_name": "Berzerk"}
    - slot{"track_artist": "Eminem"}
    - slot{"track_albumartist": "Eminem"}
    - slot{"track_composer": null}
    - slot{"track_album": "Greatest Songs"}
    - slot{"track_genre": "Rap"}
    - slot{"track_duration": "0:03:49"}
    - slot{"track_year": "2017"}
    - slot{"track_filesize": "8 MB"}

## 23_playing_music_with_track_name_and_saying_no_when_asked_anything_else
* asking_play_music{"track_name": "Superman"}
    - slot{"track_name": "Superman"}
    - action_play_music
    - slot{"music_file": "04 - Superman (Ft. Dina Rae).mp3"}
    - slot{"track_name": "Superman (Ft. Dina Rae)"}
    - slot{"track_artist": "Eminem"}
    - slot{"track_albumartist": "Eminem"}
    - slot{"track_composer": null}
    - slot{"track_album": "Greatest Songs"}
    - slot{"track_genre": "Rap"}
    - slot{"track_duration": "0:05:51"}
    - slot{"track_year": "2017"}
    - slot{"track_filesize": "13 MB"}
    - utter_do_you_need_anything_else
* saying_no
    - utter_saying_okay_to_denial

## 24_playing_music_with_track_name_and_asking_weather_for_mentioned_city
* saying_hello
    - action_greet_user
    - utter_how_can_i_help
* asking_play_music{"track_name": "Superman"}
    - slot{"track_name": "Superman"}
    - action_play_music
    - slot{"music_file": "04 - Superman (Ft. Dina Rae).mp3"}
    - slot{"track_name": "Superman (Ft. Dina Rae)"}
    - slot{"track_artist": "Eminem"}
    - slot{"track_albumartist": "Eminem"}
    - slot{"track_composer": null}
    - slot{"track_album": "Greatest Songs"}
    - slot{"track_genre": "Rap"}
    - slot{"track_duration": "0:05:51"}
    - slot{"track_year": "2017"}
    - slot{"track_filesize": "13 MB"}
    - utter_do_you_need_anything_else
* asking_weather_conditions{"city": "London"}
    - slot{"city": "London"}
    - utter_saying_fetching_weather_details
    - action_tell_current_forecast_weather_conditions
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_welcome_to_action
    - utter_do_you_need_anything_else
* saying_no
    - utter_saying_okay_to_denial

## 25_playing_music_with_track_name_and_asking_forecast_and_playing_music_again
* saying_hello{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - action_greet_user
    - utter_how_can_i_help
* asking_play_music{"track_name": "Okami"}
    - slot{"track_name": "Okami"}
    - action_play_music
    - slot{"music_file": null}
    - slot{"track_name": null}
    - slot{"track_artist": null}
    - slot{"track_albumartist": null}
    - slot{"track_composer": null}
    - slot{"track_album": null}
    - slot{"track_genre": null}
    - slot{"track_duration": null}
    - slot{"track_year": null}
    - slot{"track_filesize": null}
    - utter_do_you_need_anything_else
* asking_forecast_weather_conditions{"city": "Mumbai", "hours": "18"}
    - slot{"city": "Mumbai"}
    - slot{"hours": "18"}
    - utter_saying_fetching_weather_details
    - action_tell_forecast_weather_conditions
    - slot{"city": "Mumbai"}
    - slot{"hours": "18"}
    - slot{"minutes": null}
* saying_thank_you
    - utter_saying_welcome_to_action
    - utter_do_you_need_anything_else
* asking_play_music{"track_artist": "Chainsmokers"}
    - slot{"track_artist": "Chainsmokers"}
    - action_play_music
    - slot{"music_file": null}
    - slot{"track_name": null}
    - slot{"track_artist": null}
    - slot{"track_albumartist": null}
    - slot{"track_composer": null}
    - slot{"track_album": null}
    - slot{"track_genre": null}
    - slot{"track_duration": null}
    - slot{"track_year": null}
    - slot{"track_filesize": null}
* saying_thank_you{"ai": "charlotte"}
    - slot{"ai": "charlotte"}
    - utter_saying_welcome_to_action
    - utter_do_you_need_anything_else
* saying_no{"time": "now"}
    - slot{"time": "now"}
    - utter_saying_okay_to_denial
