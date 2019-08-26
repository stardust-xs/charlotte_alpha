"""
This module creates Master user profile.
The module captures the data from the user and saves it in an environment
variable. The data stored, is encrypted using a key which the user provides
while setting up his/her profile.

See https://github.com/xames3/charlotte for complete documentation.
"""
import os
from os import system
from random import randint
from subprocess import PIPE, Popen
from sys import exc_info, exit
from time import sleep
from os.path import exists

from twilio.rest import Client

from charlotte.setup import NAME, NUMBER
from charlotte.utils.assists.cipher import encrypt, decrypt, keygen
from charlotte.utils.assists.generic import display
from charlotte.utils.assists.inquiry import answer, confirm, secure

if os.environ.get('CHARLOTTE_DEFAULT_MASTER_KEY') is None:
    start = confirm(
        f'Hello, I\'m {NAME.title()}, your personal assistant.\n  I don\'t see'
        ' any profile in my system. Would you like me to create one now?')
    if start is False:
        display('Profile creation unsuccessful. Terminating program...')
        exit()
    else:
        warning = confirm('WARNING: Profile creation requires a'
                          ' system reboot to take effect. So please save all'
                          ' your data before proceeding.')
        if warning is True:
            if os.environ.get('CHARLOTTE_DEFAULT_MASTER_KEY') is None:
                display('Tip #0: Password should be unique, incasing at least'
                        ' 1 uppercase, 1 lowercase, 1 special character'
                        ' [!, @, \#, $, %, ^,..] and a number.')
                key = keygen(secure('Please provide a password. This password'
                                    ' will be used for all ciphering.'), return_key=True)
        else:
            display('Profile creation unsuccessful. Terminating program...')
            exit()
else:
    key_confirm = confirm('Master password detected! Would you like '
                          'to use the same password?')
    if key_confirm is True:
        key = os.environ.get('CHARLOTTE_DEFAULT_MASTER_KEY')
    else:
        key = keygen(secure('Please provide a password. This password'
                            ' will be used for all encrypting. You need to'
                            ' restart your system to show it\'s effect.'),
                     return_key=True)

try:
    display('Tip #1: All inputs should be one-worded, Eg: Sir, Ma\'am,'
            ' Charlotte, Master, XA, etc.')
    user_name_primary = encrypt(answer('How should I address you?'), key)
    name = decrypt(user_name_primary, key)
    display('Tip #2: If you don\'t want to share something OR'
            ' just want to skip a question, just press Enter.')
    user_name_secondary = encrypt(answer(f'Okay {name.lower()}. Tell me'
                                         ' what would you prefer as your'
                                         ' username?'), key)
    display('Tip #3: This is mandatory. All Phone numbers should contain the'
            ' country codes with \'+\' symbol. Eg: +9190XXXXXX52')
    user_phone_primary = encrypt((secure(f'Your primary contact number,'
                                         f' {name.lower()}?').replace('-', '').replace(' ', '')), key)
    wake_phrase = encrypt(
        answer(f'And finally {name.lower()}, how would you like '
               'to call me?'), key)
    display(
        f'{decrypt(wake_phrase, key).title()}, sounds cool! I like that.')

    otp = randint(000000000000, 999999999999)
    client = Client(os.environ.get('TWILIO_SID'),
                    os.environ.get('TWILIO_TOKEN'))
    message = client.messages.create(
        from_=f'{NUMBER}',
        to=f'{decrypt(user_phone_primary, key)}',
        body=f'{name.title()}, your verification code is : {otp}')

    match = secure(f'{name.title()}, I\'ve sent a code onto your'
                   ' phone. Please enter it to proceed.')
    if int(match) == otp:
        Popen(f"setx CHARLOTTE_DEFAULT_MASTER_KEY {key}",
              stdout=PIPE, shell=True)
        Popen(f"setx CHARLOTTE_DEFAULT_PRIMARY_NAME {user_name_primary}",
              stdout=PIPE, shell=True)
        Popen(f"setx CHARLOTTE_DEFAULT_SECONDARY_NAME {user_name_secondary}",
              stdout=PIPE, shell=True)
        Popen(f"setx CHARLOTTE_DEFAULT_PRIMARY_PHONE {user_phone_primary}",
              stdout=PIPE, shell=True)
        Popen(f"setx CHARLOTTE_DEFAULT_WAKE_PHRASE {wake_phrase}",
              stdout=PIPE, shell=True)
        Popen(f"setx CHARLOTTE_DEFAULT_MASTER_KEY {key}",
              stdout=PIPE, shell=True)
        for index in range(5, -1, -1):
            sleep(1)
            print('\r? Profile created successfully! System will restart'
                  f' in {index} seconds', end='')
        system('shutdown /r /t 1')
        exit()
    else:
        display(
            f'I\'m not able to verify you '
            f'{decrypt(user_name_secondary, key).title()}. I\'m afraid'
            ' I need to terminate myself.')
        exit()
except Exception as error:
    print('An error occured while performing this operation because of'
          f' {error} in function "{stack()[0][3]}" on line'
          f' {exc_info()[-1].tb_lineno}.')
