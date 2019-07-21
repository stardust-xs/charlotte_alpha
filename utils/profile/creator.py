"""
Global user profile for Charlotte
=================================

It creates an User profile.

See https://github.com/xames3/charlotte for complete documentation.
"""
import os
from jinja2 import Template
from os import remove
from random import randint
from sys import exit
from os.path import exists

from questionary import Choice, select

from twilio.rest import Client

from .. fluids.paths import FILE
from .. fluids.setup import NAME, NUMBER
from .. functions.assistant import age, locate
from .. functions.basics import display, quit
from .. functions.questions import answer, confirm, decide, secure
from .. security.encryption import cipher, decipher, keygen

# https://stackoverflow.com/questions/28557626/how-to-update-yaml-file-using-python
template = Template(u'''\
# User details

user_name_primary: {{ user_name_primary }}
user_name_secondary: {{ user_name_secondary }}
user_first_name: {{ user_first_name }}
user_middle_name: {{ user_middle_name }}
user_last_name: {{ user_last_name }}
user_father_name: {{ user_father_name }}
user_mother_name: {{ user_mother_name }}
user_gender: {{ user_gender }}
user_type_man: {{ user_type_man }}
user_type_woman: {{ user_type_woman }}
user_birthdate: {{ user_birthdate }}
user_age: {{ user_age }}
user_blood_type: {{ user_blood_type }}
user_phone_primary: {{ user_phone_primary }}
user_phone_secondary: {{ user_phone_secondary }}
emergency_contact_primary: {{ emergency_contact_primary }}
emergency_contact_secondary: {{ emergency_contact_secondary }}
user_father_phone_primary: {{ user_father_phone_primary }}
user_father_phone_secondary: {{ user_father_phone_secondary }}
user_mother_phone_primary: {{ user_mother_phone_primary }}
user_mother_phone_secondary: {{ user_mother_phone_secondary }}
user_email_primary: {{ user_email_primary }}
user_email_password_primary: {{ user_email_password_primary }}
user_email_secondary: {{ user_email_secondary }}
user_email_password_secondary: {{ user_email_password_secondary }}
user_facebook_handle: {{ user_facebook_handle }}
user_facebook_password: {{ user_facebook_password }}
user_instagram_handle: {{ user_instagram_handle }}
user_instagram_password: {{ user_instagram_password }}
user_twitter_handle: {{ user_twitter_handle }}
user_twitter_password: {{ user_twitter_password }}
user_skype_handle: {{ user_skype_handle }}
user_skype_password: {{ user_skype_password }}
user_home_address: {{ user_home_address }}
user_home_street: {{ user_home_street }}
user_home_city: {{ user_home_city }}
user_home_state: {{ user_home_state }}
user_home_country: {{ user_home_country }}
wake_phrase: {{ wake_phrase }}

# Built by XA
''')

if not exists(FILE['master']):
    start = confirm(
        f'Hello, I\'m {NAME.title()}, your personal assistant.\n  I don\'t see'
        ' any profile in my system. Would you like me to create one now?')
    if start is False:
        display('Profile creation unsuccessful. Terminating program...')
        exit()
    else:
        display('Tip #0: Password should be unique incasing at least 1'
                ' uppercase, 1 lowercase, 1 special character [!, @, \#,'
                ' $, %, ^,..] and a number.')

        # Key generation
        key_file = keygen(
            secure('Before we initiate user creation sequence, please'
                   ' provide a password.'))
        with open(FILE['key'], 'rb') as key_file:
            key = key_file.read()

        display('Tip #1: All inputs should be one-worded, Eg: Sir, Ma\'am,'
                ' Charlotte, Master, XA, etc.')

        # Saving data temporarily - Nickname
        user_name_primary = cipher(answer('How should I address you?'), key)
        name = decipher(user_name_primary, key)

        # Comman name\Username
        user_name_secondary = cipher(answer(f'Okay {name.lower()}. Tell me'
                                            ' what would you prefer as your'
                                            ' username?'), key)

        # Gender of the user
        user_gender = cipher(select(message=f'Thank you! And you are ?',
                                    choices=[Choice('Man', 'man'),
                                             Choice('Woman', 'woman')]).ask(), key)

        display('Perfect!')

        # First name of the user
        user_first_name = cipher(answer(f'{name.title()}, please tell me your'
                                        ' first name?'), key)

        # Middle name\Father's name\Spouse's name
        user_middle_name = cipher(answer('Alright. Your middle name?'), key)

        # Last name\Surname\Family name
        user_last_name = cipher(answer('And your last name?'), key)

        # Father's name
        father_name = decipher(user_middle_name, key)
        father_name_option = confirm(f'Is \'{father_name}\' your father\'s'
                                     ' name?')

        if father_name_option is True:
            user_father_name = user_middle_name
        else:
            user_father_name = cipher(answer(f'Your father\'s name,'
                                             ' {name.lower()}?'), key)

        # Mother's name
        user_mother_name = cipher(answer('Mother\'s name?'), key)
        mother_name = decipher(user_mother_name, key)

        # Gender calculation
        user_type_man = cipher(
            str(True if user_gender is 'man' else False), key)
        user_type_woman = cipher(
            str(True if user_gender is 'woman' else False), key)

        display('Tip #2: Birthdate should be \'YYYY-MM-DD\' format.')

        # Birthday
        user_birthdate = cipher(answer(f'{name.title()}, I need your'
                                       ' birthdate.'), key)

        # Current age in years
        user_age = cipher(str(age(decipher(user_birthdate, key))), key)

        # Blood type
        user_blood_type = cipher(select(message='Your blood type,'
                                                f' {name.lower()}?',
                                        choices=[Choice('A +ve', 'a_pos'),
                                                 Choice('A -ve', 'a_neg'),
                                                 Choice('B +ve', 'b_pos'),
                                                 Choice('B -ve', 'b_neg'),
                                                 Choice('AB +ve', 'ab_pos'),
                                                 Choice('AB -ve', 'ab_neg'),
                                                 Choice('O +ve', 'o_pos'),
                                                 Choice('O -ve', 'o_neg'),
                                                 Choice('H +ve', 'h_pos'),
                                                 Choice('H -ve', 'h_neg'),
                                                 Choice('Skip this', 'NA')
                                                 ]).ask(), key)

        display('Tip #3: All Phone numbers should contain the country'
                ' codes with \'+\' symbol. Eg: +9190XXXXXX52')

        # Primary contact
        user_phone_primary = cipher((secure(f'Your primary contact number,'
                                            f' {name.lower()}?').replace('-', '').replace(' ', '')), key)

        display('Tip #4: If you don\'t want to share something OR'
                ' just want to skip a question, just press Enter.')

        # Secondary contact
        user_phone_secondary = cipher((secure('Okay, secondary contact'
                                              ' details?').replace('-', '').replace(' ', '')), key)

        # Setting up emergency contacts
        emergency_user_option = cipher(select(message=f'{name.title()}, whom'
                                              ' would you prefer as your'
                                              ' Primary Emergency contact?', choices=[Choice(f'{father_name}', 'user_father_name'), Choice(f'{mother_name}', 'user_mother_name')]).ask(), key)

        if emergency_user_option is 'user_father_name':
            emergency_contact_primary = user_father_name
            emergency_contact_secondary = user_mother_name
        else:
            emergency_contact_primary = user_mother_name
            emergency_contact_secondary = user_father_name

        # Father's primary number
        user_father_phone_primary = cipher((secure(
            'Your father\'s primary contact details?').replace('-', '').replace(' ', '')), key)

        # Father's secondary number
        user_father_phone_secondary = cipher((secure(
            f'His secondary contact details, {name.lower()}?').replace('-', '').replace(' ', '')), key)

        # Mother's primary number
        user_mother_phone_primary = cipher((secure(
            'Your mother\'s primary contact details?').replace('-', '').replace(' ', '')), key)

        # Mother's secondary number
        user_mother_phone_secondary = cipher((secure(
            f'And her secondary contact details, {name.lower()}?').replace('-', '').replace(' ', '')), key)

        # Primary email
        user_email_primary = cipher(secure('Your email address?'), key)

        # Primary email password
        user_email_password_primary = cipher(secure('It\'s password?'), key)

        # Secondary email
        user_email_secondary = cipher(secure('Secondary email address,'
                                             f' {name.lower()}?'), key)

        # Secondary email password
        user_email_password_secondary = cipher(
            secure('And it\'s password?'), key)

        # Facebook handle
        user_facebook_handle = cipher(decide(
            f'Do you have a Facebook account, {name.lower()}?', 'What is it\'s username?'), key)

        # Facebook  password
        if decipher(user_facebook_handle, key) != 'NA':
            user_facebook_password = cipher(
                secure('Alright it\'s password?'), key)
        else:
            user_facebook_password = cipher('NA', key)

        # Instagram handle
        user_instagram_handle = cipher(decide(
            f'Do you have an account on Instagram?', 'What\'s it\'s user id?'), key)

        # Instagram password
        if decipher(user_instagram_handle, key) != 'NA':
            user_instagram_password = cipher(
                secure('And it\'s password?'), key)
        else:
            user_instagram_password = cipher('NA', key)

        # Twitter handle
        user_twitter_handle = cipher(
            decide('Are you on Twitter?', 'What is it\'s username?'), key)

        # Twitter  password
        if decipher(user_twitter_handle, key) != 'NA':
            user_twitter_password = cipher(secure('It\'s password?'), key)
        else:
            user_twitter_password = cipher('NA', key)

        # Skype handle
        user_skype_handle = cipher(decide(
            f'Do you have Skype account?', 'What\'s it\'s user id?'), key)

        # Skype password
        if decipher(user_skype_handle, key) != 'NA':
            user_skype_password = cipher(secure('And it\'s password?'), key)
        else:
            user_skype_password = cipher('NA', key)

        display('Tip #5: Hold steady...')

        # Tracking location
        display('I\'m locating your position...')
        user_home_address = cipher(locate(), key)
        user_home_street = cipher(locate('street'), key)
        user_home_city = cipher(locate('city'), key)
        user_home_state = cipher(locate('state'), key)
        user_home_country = cipher(locate('country'), key)
        display('Got it!')

        # AI name
        wake_phrase = cipher(
            answer(f'And finally {name.lower()}, how would you like '
                   'to call me?'), key)
        display(
            f'{decipher(wake_phrase, key).title()}, sounds cool! I like that.')

        details = template.render(user_name_primary=user_name_primary,
                                  user_name_secondary=user_name_secondary,
                                  user_gender=user_gender,
                                  user_first_name=user_first_name,
                                  user_middle_name=user_middle_name,
                                  user_last_name=user_last_name,
                                  user_father_name=user_father_name,
                                  user_mother_name=user_mother_name,
                                  user_type_man=user_type_man,
                                  user_type_woman=user_type_woman,
                                  user_birthdate=user_birthdate,
                                  user_age=user_age,
                                  user_blood_type=user_blood_type,
                                  user_phone_primary=user_phone_primary,
                                  user_phone_secondary=user_phone_secondary,
                                  emergency_contact_primary=emergency_contact_primary,
                                  emergency_contact_secondary=emergency_contact_secondary,
                                  user_father_phone_primary=user_father_phone_primary,
                                  user_father_phone_secondary=user_father_phone_secondary,
                                  user_mother_phone_primary=user_mother_phone_primary,
                                  user_mother_phone_secondary=user_mother_phone_secondary,
                                  user_email_primary=user_email_primary,
                                  user_email_password_primary=user_email_password_primary,
                                  user_email_secondary=user_email_secondary,
                                  user_email_password_secondary=user_email_password_secondary,
                                  user_facebook_handle=user_facebook_handle,
                                  user_facebook_password=user_facebook_password,
                                  user_instagram_handle=user_instagram_handle,
                                  user_instagram_password=user_instagram_password,
                                  user_twitter_handle=user_twitter_handle,
                                  user_twitter_password=user_twitter_password,
                                  user_skype_handle=user_skype_handle,
                                  user_skype_password=user_skype_password,
                                  user_home_address=user_home_address,
                                  user_home_street=user_home_street,
                                  user_home_city=user_home_city,
                                  user_home_state=user_home_state,
                                  user_home_country=user_home_country,
                                  wake_phrase=wake_phrase)

        otp = randint(000000, 999999)
        client = Client(os.environ.get('TWILIO_SID'),
                        os.environ.get('TWILIO_TOKEN'))
        message = client.messages.create(
            from_=f'{NUMBER}',
            to=f'{decipher(user_phone_primary, key)}',
            body=f'{name.title()}, your verification code is : {otp}')

        match = secure(f'{name.title()}, I\'ve sent an SMS onto your'
                       ' phone. Please enter it to proceed.')
        if int(match) == otp:
            with open(FILE['master'], 'w') as profile:
                profile.write(details)
            display(f'Profile created. {name.title()}, I\'m ready!')
        else:
            display(
                f'I\'m not able to verify you {decipher(user_first_name, key).title()}. I\'m afraid I need to terminate myself.')
            remove(FILE['key'])
            exit()
