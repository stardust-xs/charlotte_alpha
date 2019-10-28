"""
The profile module: Creates and represents profile of main user.

The module stores data in an environment variables. The data stored, is
encrypted using a key which is provided while setting up profile.

See https://github.com/xames3/charlotte for complete documentation.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.1 - Program sleeps after printing the restart warning, instead
#           of sleeping before.
#           Made the code more* PEP-8 compliant.
#   1.0.2 - Added comments for alias and assistant name.
#   1.0.0 - First code.

import os
from inspect import stack
from os import system
from random import randint
from subprocess import PIPE, Popen
from sys import exc_info, exit
from time import sleep

from twilio.rest import Client

from charlotte.setup import NAME, NUMBER
from charlotte.utils.assists.cipher import encrypt, decrypt, keygen
from charlotte.utils.assists.generic import show
from charlotte.utils.assists.inquiry import answer, confirm, secure

# Constant used to store the main master password for ciphering.
# This key or password is used to for ciphering all the strings used in
# this package.
_MASTER_KEY = 'CHARLOTTE_MASTER_KEY'
# Constant used to store alias name for calling.
# Alias is required to call the user with nickname or designation.
_ALIAS = 'XA_ALIAS'
# Constant used to store the username.
# This is the primary name of the user.
_USERNAME = 'XA_USERNAME'
# Constant used to store the mobile number.
# This is required to send SMS, for verification purposes.
_MOBILE = 'XA_MOBILE'
# Constant used to store AI invoke name.
# By using this name, Charlotte will be activated.
_HOTWORD = 'XA_HOTWORD'
# Constant used for showing tip #1.
# This tip is regarding password setup.
_TIP_1 = 'Tip #1: Password should be unique, with at least 1 uppercase, 1 ' \
    'lowercase, 1 special character [!, @, #, $, %, ^,..] and a number.'
# Constant used for showing tip #2.
# This tip is regarding giving an aliad name.
_TIP_2 = 'Tip #2: All inputs should be one-worded, for e.g: Sir, Ma\'am, ' \
    'Boss, Master, XA, etc.'
# Constant used for showing tip #3.
# This tip is regarding skipping a question.
_TIP_3 = 'Tip #3: If you do not want to share something or just want to ' \
    'skip a question, just press Enter.'
# Constant used for showing tip #4.
# This tip is regarding providing mobile number.
_TIP_4 = 'Tip #4: This is mandatory. Mobile number should contain the ' \
    'country codes with "+" symbol. Eg: +9190XXXXXX52'
# Constant used to wish the user for initial setup.
_INITIAL_SETUP = f'Hello, I\'m {NAME.title()}, your personal assistant.\n  ' \
    'I do not see any profile in my system. Would you like me to create one ' \
    'now?'
# Constant used to respond if the process of profile creation is
# skipped.
_PROFILE_SKIPPED = 'Profile creation unsuccessful. Terminating program...'
# Constant used to warn regarding the upcoming system restart.
_RESTART_REQUIRED = 'WARNING: Profile creation requires a system reboot to ' \
    'take effect. So please save all your data before proceeding.'
# Constant used to take the master password.
_GIVE_PASSWORD = 'Please provide a password. This password will be used ' \
    'for all ciphering.'
# Constant used to respond if password exists already in environment
# variable.
_PASSWORD_DETECTED = 'Master password detected! Would you like to use the ' \
    'same password?'
# Constant used to warn regarding the applicability of the password
# after the system restart.
_PASSWORD_RESTART = 'Please provide a password. This password will be used ' \
    'for all encrypting. You need to restart your system to show it\'s effect.'
# Constant used to ask the alias.
_ASK_ALIAS = 'What should I call you?'
# Constant used to ask the username.
_ASK_USERNAME = 'Okay. Tell me what would you prefer as your username?'
# Constant used to ask the mobile number.
_ASK_MOBILE = 'Your mobile number?'
# Constant used to ask the hotword.
_ASK_HOTWORD = f'And finally, how would you like to call me?'
# Constant used to ask for OTP.
_ENTER_OTP = 'I have sent a code onto your phone. Please enter it to proceed.'
# Constant used to respond if the user verification is failed.
_RECOGNIZE_FAILURE = 'I could not verify you. I am afraid I must terminate '\
    'this session.'

# Code starts here:
# Checks if all the necessary environment variables are present or not.
try:
    if all([os.environ.get(_MASTER_KEY),
            os.environ.get(_ALIAS),
            os.environ.get(_USERNAME),
            os.environ.get(_MOBILE),
            os.environ.get(_HOTWORD)]) is False:
        show('Key check failed! Creating user profile.')
        # If no master key is detected.
        if os.environ.get(_MASTER_KEY) is None:
            start = confirm(_INITIAL_SETUP)
            if start is False:
                show(_PROFILE_SKIPPED)
                exit()
            else:
                warning = confirm(_RESTART_REQUIRED)
                if warning is True:
                    if os.environ.get(_MASTER_KEY) is None:
                        show(_TIP_1)
                        key = keygen(_MASTER_KEY,
                                     secure(_GIVE_PASSWORD), return_key=True)
                else:
                    show(_PROFILE_SKIPPED)
                    exit()
        else:
            # If master key already exists.
            key_confirm = confirm(_PASSWORD_DETECTED)
            if key_confirm is True:
                key = os.environ.get(_MASTER_KEY)
            else:
                key = keygen(_MASTER_KEY,
                             secure(_PASSWORD_RESTART), return_key=True)
        show(_TIP_2)
        alias = encrypt(answer(_ASK_ALIAS), key)
        show(_TIP_3)
        username = encrypt(answer(_ASK_USERNAME), key)
        name = decrypt(username, key)
        show(_TIP_4)
        mobile = encrypt((secure(_ASK_MOBILE)).replace(
            '-', '').replace(' ', ''), key)
        hotword = encrypt(answer(_ASK_HOTWORD), key)
        show(f'{decrypt(hotword, key).title()}, seems nice! I like that.')
        # OTP verification using Twilio.
        # Creating a random 12-digit number for SMS verification.
        otp = randint(000000000000, 999999999999)
        client = Client(os.environ.get('TWILIO_SID'),
                        os.environ.get('TWILIO_TOKEN'))
        message = client.messages.create(
            from_=f'{NUMBER}',
            to=f'{decrypt(mobile, key)}',
            body=f'{name.title()}, your verification code is: {otp}')
        match = secure(_ENTER_OTP)
        if int(match) == otp:
            # If OTP matches write into environment variables,
            # terminates the process.
            Popen(f"setx {_MASTER_KEY} {key}", stdout=PIPE, shell=True)
            Popen(f"setx {_ALIAS} {alias}", stdout=PIPE, shell=True)
            Popen(f"setx {_USERNAME} {username}", stdout=PIPE, shell=True)
            Popen(f"setx {_MOBILE} {mobile}", stdout=PIPE, shell=True)
            Popen(f"setx {_HOTWORD} {hotword}", stdout=PIPE, shell=True)
            for index in range(5, -1, -1):
                print('\r? Profile created successfully! System will restart'
                      f' in {index} seconds', end='')
                sleep(1)
            system('shutdown /r /t 1')
            exit()
        else:
            show(_RECOGNIZE_FAILURE)
            exit()
    else:
        key = os.environ.get(_MASTER_KEY)
        alias = decrypt(os.environ.get(_ALIAS), key)
        username = decrypt(os.environ.get(_USERNAME), key)
        mobile = decrypt(os.environ.get(_MOBILE), key)
        hotword = decrypt(os.environ.get(_HOTWORD), key)
        # Lower and Title case alias of the main user.
        # This is used for all future interactions with primary user.
        lower = alias.lower()
        title = alias.title()
        # Lower and Title case name of the assistant.
        # This name would be used for calling the assistant.
        ai_lower = hotword.lower()
        ai_title = hotword.title()
except Exception as error:
    print('An error occured while performing this operation because of'
          f' {error} in function "{stack()[0][3]}" on line'
          f' {exc_info()[-1].tb_lineno}.')
