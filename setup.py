"""
The setup module: Represents Charlotte`s current package status.

This module will help to understand the developments happening in the
package. It also stores the logs of the changes that happen within the
program with a timestamp that signifies from when the changes were made
to before pushing it to Github.

At a glance, the structure of the module is following:
 - NAME:                Name of Natural Language UI Assistant.
 - CODENAME:            Codename for Assistant (For internal reference).
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
#   1.1.1 - Updated to 1.1.1 - 7, October 2019 - MAJOR RELEASE
#           - Made all the script more PEP-8 compliant - This is a major
#             change.
#           - Added type hints to all the scripts except connect, run &
#             actions.py.
#           - requirements.txt now has GCS, Django and pyTTSx3 modules.
#           - domain.yml is reduced to just weather related domain.
#           - .gitignore now has updated directory & file structure.
#           - config.yml is updated to process more data & history.
#           - Reduced the redundancies in rasa.py.
#           - profile.py sleeps after the warning & restarts the system.
#           - Added `resolve_days` & `profiler` functions to system.py.
#           - Updated paths as per new configuration in directories.py.
#           - Reworked & optimized weather.py from ground up. Added type
#             hints and new functions for better search results.
#           - weather.py now uses DarkSky for weather api calls.
#   1.1.0 - Updated to 1.1.0 - 4, October 2019
#           - Reworked nlu.md, actions.py, weather.py, domain.yml from
#             ground up - This is a major change.
#           - weather.py now checks internet before making an API call.
#           - New constants are added for handling Imperial system in
#             `weather.py` module.
#           - weather.py has replaced the old functions in favor for
#             new ones.
#           - `_predict()` in weather.py now has more natural responses
#             for weather predictions.
#           - nlu.md data is now cleaned off from all redundancies & now
#             uses `querying` suffix instead of `asking` for intents.
#           - Also, examples to retrieve weather details in imperial
#             have been added. This has helped to overcome Overfitting.
#           - Stories are removed for now and are accessed through it`s
#             own directory which is added in directory.py under
#             ./data/stories/.
#           - All the variables that were used are replaced with
#             dictionaries in phrases.py.
#           - Added explicit `make_dir` command while evaluating models
#             in rasa.py.
#           - Deleted ./dump/ directory in favor of ./tests/ & ./temp/.
#           - Reference link to ./dump/ is removed from .gitignore file.
#           - ./bin/ directory is also now added to the .gitignore file.
#           - Added key for ./reserves/ in directories.py.
#   1.0.7 - Updated to 1.0.7 - 27, September 2019 (UNRELEASED)
#           - Downgraded rasa and rasa_sdk from 1.3.x builds to 1.2.x
#             with TF-GPU 1.3.2 installed - This is a major change.
#           - requirements.txt is updated with correct rasa & TF builds.
#           - Downloaded spacy model using
#             python -m spacy download en_core_web_md.
#           - Fixed a typo in weather.py.
#           - Added one more phrase in phrases.py.
#   1.0.6 - Updated to 1.0.6 - 25, September 2019
#           - Using TF-GPU is discontinued - This is a major change.
#           - Upgraded to rasa & rasa_sdk to 1.3.6 & 1.3.2 respectively
#             with TF v1.14.0.
#           - Updated requirements.txt to download updated packages.
#           - Tensorflow-GPU is now removed from requirements.txt file.
#           - `MaxHistoryTrackerFeaturizer` is commented to handle bug
#             with history tracking in Rasa.
#           - Added boolean slots for checking conditions at inference
#             in domain.yml file.
#           - Phrases are accessed using the dictionaries instead of
#             variables in phrases.py.
#           - Comments updated in rasa.py.
#           - run.py now uses dictionaries for displaying CLI phrases.
#   1.0.5 - Updated to 1.0.5 - 18, September 2019
#           - Updated the slots in domain.yml file.
#           - `wish_user` is now changed to `greet_user` in person.py
#             module.
#           - `greet_user` now returns current time, hour & minutes
#             along with greetings in person.py.
#           - Renamed sandbox directory to dump. Corrected in .gitignore
#             file.
#   1.0.4 - Updated to 1.0.4 - 16, September 2019
#           - Downgraded rasa and rasa_sdk from 1.3.0 and higher builds
#             to rasa==1.2.8 & rasa_sdk==1.2.0 - This is a major change.
#           - requirements.txt file now has only the essential packages.
#           - Added hyphenated indents in setup.py history section.
#           - Downloaded spacy model using
#             python -m spacy download en_core_web_lg.
#           - Added few more examples in nlu.md data file.
#           - Exception handling in actions.py is replaced with if-else.
#           - Added 1 more example and fixed typo in phrases.py.
#           - Added new function, `check_internet` in system.py.
#           - person.py now uses `check_internet` function while
#             locating the user location.
#           - weather.py now uses `check_internet` function while
#             finding the weather-forecast details.
#           - Added support comments while returning None in weather.py.
#   1.0.3 - Updated to 1.0.3 - 8, September 2019
#           - Added support for virtual environment - This is a major
#             change.
#           - Fixed connector code in connect.py.
#           - Deprecated `select` and used `choose` instead in run.py.
#           - Added new phrase, `no_internet_connection` in phrases.py.
#           - Added error handling on no internet in actions.py.
#           - actions.py now supports exception handling if no internet
#             is detected.
#           - Added warning for model overwriting in rasa.py.
#           - Corrected typos in setup.py.
#           - weather.py now returns None if exceptions are raised.
#           - Added few more examples in nlu.md data file.
#           - ngrok.exe can be accessed through files.py.
#   1.0.2 - Updated to 1.0.2 - 7, September 2019
#           - Updated rasa to 1.3.0 & rasa_sdk to 1.3.2 - This is major
#             change.
#           - Updated requirements.txt to match new rasa requirements
#             (including tensorflow/tensorflow-gpu v1.14.0).
#           - Added brief introduction to setup.py.
#           - Reduced unnecessary use of "`" in comments for simplicity
#             from multiple files.
#           - Fixed typo in weather.py.
#           - Fixed error caused by not importing `os.walk` in music.py.
#           - Added support for previous and next track in music.py.
#             music.py now uses fuzzy matcher while finding next and
#             previous tracks.
#           - `music_file` slot is now set in actions.py.
#           - Added `show` and removed unused import in rasa.py.
#           - Added `select_file` function in inquiry.py.
#           - Added comments in profile.py.
#   1.0.1 - Updated to 1.0.1 - 6, September 2019
#           - Updated inquiry.py by adding `choose` function, rasa.py by
#             adding links to reference code in function and updated
#             main docstring of setup.py.
#   1.0.0 - First code - 5, September 2019

import os

NAME = 'charlotte'

CODENAME = 'lazuli'

NUMBER = os.environ.get('CHARLOTTE_NUMBER')

VERSION = '1.1.1'

AUTHOR = MAINTAINER = 'XAMES3'

AUTHOR_EMAIL = MAINTAINER_EMAIL = 'xames3.charlotte@gmail.com'

DOCS_BASE_URL = GITHUB_URL = 'https://github.com/xames3/charlotte'

LICENSE = 'GNU General Public License v3.0'
