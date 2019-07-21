"""
Global user details for Charlotte
=================================

Reads the encrypted user profile details stored in `./users/profile.yml` file.

See https://github.com/xames3/charlotte for complete documentation.
"""
from os.path import exists
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .. security.encryption import decipher
from .. fluids.paths import FILE

if not exists(FILE['key']):
    from .. functions.basics import display

    display('Key check failed! Creating user profile.')
    from . creator import *
else:
    if not exists(FILE['master']):
        from . creator import *

profile = load(open(FILE['master']), Loader=Loader)
with open(FILE['key'], 'rb') as key_file:
    key = key_file.read()

primary = decipher(profile['user_name_primary'], key)
secondary = decipher(profile['user_name_secondary'], key)
first_name = decipher(profile['user_first_name'], key)
middle_name = decipher(profile['user_middle_name'], key)
last_name = decipher(profile['user_last_name'], key)
father_name = decipher(profile['user_father_name'], key)
mother_name = decipher(profile['user_mother_name'], key)
gender = decipher(profile['user_gender'], key)
man = decipher(profile['user_type_man'], key)
woman = decipher(profile['user_type_woman'], key)
birthdate = decipher(profile['user_birthdate'], key)
age = decipher(profile['user_age'], key)
blood_type = decipher(profile['user_blood_type'], key)
phone_primary = decipher(profile['user_phone_primary'], key)
phone_secondary = decipher(profile['user_phone_secondary'], key)
emergency_contact_primary = decipher(profile['emergency_contact_primary'], key)
emergency_contact_secondary = decipher(
    profile['emergency_contact_secondary'], key)
father_phone_primary = decipher(profile['user_father_phone_primary'], key)
father_phone_secondary = decipher(profile['user_father_phone_secondary'], key)
mother_phone_primary = decipher(profile['user_mother_phone_primary'], key)
mother_phone_secondary = decipher(profile['user_mother_phone_secondary'], key)
email_primary = decipher(profile['user_email_primary'], key)
email_password_primary = decipher(profile['user_email_password_primary'], key)
email_secondary = decipher(profile['user_email_secondary'], key)
email_password_secondary = decipher(
    profile['user_email_password_secondary'], key)
facebook_handle = decipher(profile['user_facebook_handle'], key)
facebook_password = decipher(profile['user_facebook_password'], key)
instagram_handle = decipher(profile['user_instagram_handle'], key)
instagram_password = decipher(profile['user_instagram_password'], key)
twitter_handle = decipher(profile['user_twitter_handle'], key)
twitter_password = decipher(profile['user_twitter_password'], key)
skype_handle = decipher(profile['user_skype_handle'], key)
skype_password = decipher(profile['user_skype_password'], key)
address = decipher(profile['user_home_address'], key)
street = decipher(profile['user_home_street'], key)
city = decipher(profile['user_home_city'], key)
state = decipher(profile['user_home_state'], key)
country = decipher(profile['user_home_country'], key)
wake_phrase = decipher(profile['wake_phrase'], key)
lower = primary.lower()
title = primary.title()
ai_lower = wake_phrase.lower()
ai_title = wake_phrase.title()
