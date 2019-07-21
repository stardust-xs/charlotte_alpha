## play_music_with_genre
* saying_hello
    - utter_saying_hello
* asking_play_music_with_genre{"genre": "dubstep"}
    - slot{"genre": "dubstep"}
    - utter_play_music_with_genre
    - action_play_any_music

## play_any_music
* asking_play_any_music
    - utter_playing_any_music
    - action_play_any_music
