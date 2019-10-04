"""
The setup module: Represents Charlotte`s current package status.

This module will help to understand the developments happening in the package.
It also stores the logs of the changes that happen within the program with a
timestamp that signifies from when the changes were made to before pushing it
to Github.

At a glance, the structure of the module is following:
 - NAME:                Name of Natural Language UI Assistant.
 - CODENAME:            Codename for the Assistant (For internal reference).
 - NUMBER:              Contact number of the Assistant (Twilio Number).
 - VERSION:             Current version of the package.
 - AUTHOR:              Developer of the package.
 - MAINTAINER:          Maintainer of the package.
 - AUTHOR_EMAIL:        Email address of the developer.
 - MAINTAINER_EMAIL:    Email address of the maintainer.
 - DOCS_BASE_URL:       Documentation URL.
 - GITHUB_URL:          Github repository URL.
 - LICENSE:             Licensed under details.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.0 - Updated to 1.1.0 - 4, October 2019
#           - Reworked nlu.md, actions.py, weather.py, domain.yml from ground
#             up - This is a major change.
#           - weather.py now checks the internet before making an API call.
#           - New constants are added for handling Imperial metric system in
#             `weather.py` module.
#           - weather.py has replaced the old functions in favor for new ones.
#           - `_predict()` in weather.py now has more natural responses for
#             weather predictions.
#           - nlu.md data is now cleaned off from all redundancies and now uses
#             `querying` suffix instead of `asking` for its intents.
#           - Also, examples to retrieve weather details in imperial have been
#             added. This has helped to overcome Overfitting.
#           - Stories are removed for now and are accessed through it`s own
#             directory which is added in directory.py under ./data/stories/.
#           - All the variables that were used are replaced with dictionaries
#             in phrases.py module.
#           - Added explicit `make_dir` command while evaluating models in
#             rasa.py module.
#           - Deleted ./dump/ directory in favor of ./tests/ and ./temp/.
#           - Reference link to ./dump/ is removed from .gitignore file.
#           - ./bin/ directory is also now added to the .gitignore file.
#           - Added key for ./reserves/ in directories.py module.
#   1.0.7 - Updated to 1.0.7 - 27, September 2019 (UNRELEASED)
#           - Downgraded rasa and rasa_sdk from 1.3.x builds to 1.2.x builds
#             with TF-GPU 1.3.2 installed - This is a major change.
#           - requirements.txt file is updated with correct rasa and TF builds.
#           - Downloaded spacy model - python -m spacy download en_core_web_md.
#           - Fixed a typo in weather.py module.
#           - Added one more phrase in phrases.py module.
#   1.0.6 - Updated to 1.0.6 - 25, September 2019
#           - Using TF-GPU is discontinued from now - This is a major change.
#           - Upgraded to rasa and rasa_sdk to 1.3.6 and 1.3.2 respectively
#             with TF v1.14.0.
#           - Updated requirements.txt to download few of the updated packages.
#           - Tensorflow-GPU is now removed from requirements.txt file.
#           - `MaxHistoryTrackerFeaturizer` is commented to handle bug with
#             history tracking in Rasa.
#           - Added boolean slots for checking conditions at inference in
#             domain.yml file.
#           - Phrases are accessed using the dictionaries instead of variables
#             in phrases.py module.
#           - Comments updated in rasa.py module.
#           - run.py now uses dictionaries for displaying output phrases.
#   1.0.5 - Updated to 1.0.5 - 18, September 2019
#           - Updated the slots in domain.yml file.
#           - `wish_user` is now changed to `greet_user` in person.py module.
#           - `greet_user` now returns current time, hour & minutes along with
#             greetings in person.py module.
#           - Renamed sandbox directory to dump. Corrected in .gitignore file.
#   1.0.4 - Updated to 1.0.4 - 16, September 2019
#           - Downgraded rasa and rasa_sdk from 1.3.0 and higher builds to
#             rasa==1.2.8 and rasa_sdk==1.2.0 builds - This is a major change.
#           - requirements.txt file now has only the essential packages.
#           - Added hyphenated indents in setup.py history section.
#           - Downloaded spacy model - python -m spacy download en_core_web_lg.
#           - Added few more examples in nlu.md data file.
#           - Exception handling in actions.py is now replaced with if-else.
#           - Added one more example and fixed typo in phrases.py module.
#           - Added new function, `check_internet` in system.py module.
#           - person.py now uses `check_internet` function while locating the
#             user location.
#           - weather.py now uses `check_internet` function while finding the
#             weather-forecast details.
#           - Added support comments while returning None in weather.py module.
#   1.0.3 - Updated to 1.0.3 - 8, September 2019
#           - Added support for virtual environment - This is a major change.
#           - Fixed connector code in connect.py module.
#           - Deprecated `select` and used `choose` instead in run.py module.
#           - Added new phrase, `no_internet_connection` in phrases.py module.
#           - Added error handling on no internet in actions.py module.
#           - actions.py now supports exception handling if no internet is
#             detected.
#           - Added warning for model overwriting in rasa.py module.
#           - Corrected typos in setup.py module.
#           - weather.py now returns None if exceptions are raised.
#           - Added few more examples in nlu.md data file.
#           - ngrok.exe can be accessed through files.py module.
#   1.0.2 - Updated to 1.0.2 - 7, September 2019
#           - Updated rasa to 1.3.0 & rasa_sdk to 1.3.2 - This is major change.
#           - Updated requirements.txt to match new rasa requirements
#             (including tensorflow/tensorflow-gpu v1.14.0).
#           - Added brief introduction to setup.py module.
#           - Reduced unnecessary use of "`" in comments for simplicity from
#             multiple files.
#           - Fixed typo in weather.py module.
#           - Fixed error caused by not importing `os.walk` in music.py module.
#           - Added support for previous and next track in music.py module.
#             music.py now uses fuzzy matcher while finding next and previous
#             tracks.
#           - `music_file` slot is now set in actions.py module.
#           - Added `show` and removed unused import in rasa.py module.
#           - Added `select_file` function in inquiry.py module.
#           - Added comments in profile.py module.
#   1.0.1 - Updated to 1.0.1 - 6, September 2019
#           - Updated inquiry.py by adding `choose` function, rasa.py by
#             adding links to reference code in function and updated main
#             docstring of setup.py module.
#   1.0.0 - First code - 5, September 2019

import os

NAME = 'charlotte'

CODENAME = 'lazuli'

NUMBER = os.environ.get('CHARLOTTE_NUMBER')

VERSION = '1.1.0'

AUTHOR = MAINTAINER = 'XAMES3'

AUTHOR_EMAIL = MAINTAINER_EMAIL = 'xames3.charlotte@gmail.com'

DOCS_BASE_URL = GITHUB_URL = 'https://github.com/xames3/charlotte'

LICENSE = 'GNU General Public License v3.0'
