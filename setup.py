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
#   1.0.2 - Updated to 1.0.2 - 7, September 2019
#           Updated rasa to 1.3.0 and rasa_sdk to 1.3.2.
#           Updated requirements.txt to match new rasa requirements (including
#           tensorflow/tensorflow-gpu v1.14.0).
#           Added brief introduction to setup.py module.
#           Reduced unnecessary use of "`" in comments for simplicity from
#           multiple files.
#           Fixed typo in weather.py.
#           Fixed error caused by not importing `os.walk` in music.py.
#           Added support for previous and next track in music.py.
#           Added support for fuzzy finder in music.py while finding next
#           and previous tracks.
#           Setting slot, `music_file` in actions.py.
#           Added show and removed unused import in rasa.py
#           Added comments in profile.py.
#           Added `select_file` function in inquiry.py
#   1.0.1 - Updated to 1.0.1 - 6, September 2019
#           Updated inquiry.py by adding `choose` function, rasa.py by
#           adding links to reference code in function and updated main
#           docstring of setup.py.
#   1.0.0 - First code.

import os

NAME = 'charlotte'

CODENAME = 'lazuli'

NUMBER = os.environ.get('CHARLOTTE_NUMBER')

VERSION = '1.0.2'

AUTHOR = MAINTAINER = 'XAMES3'

AUTHOR_EMAIL = MAINTAINER_EMAIL = 'xames3.charlotte@gmail.com'

DOCS_BASE_URL = GITHUB_URL = 'https://github.com/xames3/charlotte'

LICENSE = 'GNU General Public License v3.0'
