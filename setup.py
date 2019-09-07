"""
The setup module: Represents Charlotte`s current package status.

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
#   1.0.1 - Updated to 1.0.1 - 6, September 2019
#           Updated `inquiry.py` by adding `choose` function, `rasa.py` by
#           adding links to reference code in function and updated main
#           docstring of `setup.py`.
#   1.0.0 - First code.

import os

NAME = 'charlotte'

CODENAME = 'lazuli'

NUMBER = os.environ.get('CHARLOTTE_NUMBER')

VERSION = '1.0.1'

AUTHOR = MAINTAINER = 'XAMES3'

AUTHOR_EMAIL = MAINTAINER_EMAIL = 'xames3.charlotte@gmail.com'

DOCS_BASE_URL = GITHUB_URL = 'https://github.com/xames3/charlotte'

LICENSE = 'GNU General Public License v3.0'
