"""
Charlotte Setup Module
======================

This module represents Charlotte`s current package status.

Attributes
    NAME            : Name of Conversational Assistant
    CODENAME        : Codename for the Assistant (For internal reference only)
    NUMBER          : Contact number of the Assistant (Twilio Trial Number)
    VERSION         : Current version of the package
    AUTHOR          : Developer of the package
    MAINTAINER      : Maintainer of the package
    AUTHOR_EMAIL    : Email address of the developer
    MAINTAINER_EMAIL: Email address of the maintainer
    DOCS_BASE_URL   : Documentation URL
    GITHUB_URL      : Github repository URL
    LICENSE         : Licensed under details

See https://github.com/xames3/charlotte for cloning the repository.
"""
import os

NAME = 'charlotte'

CODENAME = 'lazuli'

NUMBER = os.environ.get('CHARLOTTE_NUMBER')

VERSION = '1.0.2 (beta)'

AUTHOR = MAINTAINER = 'XAMES3'

AUTHOR_EMAIL = MAINTAINER_EMAIL = 'xames3.developer@gmail.com'

DOCS_BASE_URL = GITHUB_URL = 'https://github.com/xames3/charlotte'

LICENSE = 'GNU General Public License v3.0'
