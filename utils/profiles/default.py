"""
This module contains an object that represents Master User.

See https://github.com/xames3/charlotte for complete documentation.
"""
import os
from sys import exc_info

from charlotte.utils.assists.cipher import decrypt

if all([os.environ.get('CHARLOTTE_DEFAULT_MASTER_KEY'),
        os.environ.get('CHARLOTTE_DEFAULT_PRIMARY_NAME'),
        os.environ.get('CHARLOTTE_DEFAULT_SECONDARY_NAME'),
        os.environ.get('CHARLOTTE_DEFAULT_PRIMARY_PHONE'),
        os.environ.get('CHARLOTTE_DEFAULT_WAKE_PHRASE')]) is False:
    from charlotte.utils.assists.generic import display

    display('Key check failed! Creating user profile.')
    from charlotte.utils.profiles.create import *
else:
    try:
        key = os.environ.get('CHARLOTTE_DEFAULT_MASTER_KEY')
        primary = decrypt(os.environ.get(
            'CHARLOTTE_DEFAULT_PRIMARY_NAME'), key)
        secondary = decrypt(os.environ.get(
            'CHARLOTTE_DEFAULT_SECONDARY_NAME'), key)
        phone_primary = decrypt(os.environ.get(
            'CHARLOTTE_DEFAULT_PRIMARY_PHONE'), key)
        wake_phrase = decrypt(os.environ.get(
            'CHARLOTTE_DEFAULT_WAKE_PHRASE'), key)
        lower = primary.lower()
        title = primary.title()
        ai_lower = wake_phrase.lower()
        ai_title = wake_phrase.title()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
