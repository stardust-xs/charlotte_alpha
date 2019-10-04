"""
The phrases module: Replies with responses at inference.

This module is for returning random replies for particular task on the command
line.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.0 - Changed all variables into dictionary values.
#   1.0.7 - Added one more phrase in weather_protocol[`retrying`].
#   1.0.6 - Replaced all options into respective dictionaries for better
#           handling.
#   1.0.5 - Updated `wish_user` to `greet_user`.
#   1.0.4 - Added one example to `no_internet_connection` and fixed typo in it.
#   1.0.3 - Added new phrase option, `no_internet_connection`.
#   1.0.2 - Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from inspect import stack
from random import choice
from sys import exc_info

from charlotte.utils.assists.profile import ai_lower, ai_title, lower, title

try:
    # For greetings.
    greetings_protocol = {
        'morning': [f'Good Morning, {title}.', 'Good Morning!'],
        'afternoon': [f'Good Afternoon, {title}.', 'Good Afternoon!'],
        'evening': [f'Good Evening, {title}.', 'Good Evening!'],
        'night': [f'Hello, {title}!', f'Welcome back, {title}.'],
        'yes_boss': [f'{title}?', f'Yes, {lower}?']}
    # For handling options on command prompt.
    cmdline_options = {
        'greetings': ['How can I assist you?',
                      'How can I help you?',
                      'What would you like me to do?',
                      'What can I help you with?',
                      'What can I do for you?',
                      'How may I help you?'],
        'choose_model': ['Which model you want to consider?',
                         f'Which model, {lower}?',
                         f'Alright. Which model, {lower}?',
                         f'Which model you want to use, {lower}?'],
        'confirm_quit': ['Are you sure about leaving?',
                         f'Are you sure, {lower}?',
                         f'Shall I terminate this session, {lower}?',
                         f'{title}, are you sure about this?',
                         f'Are you sure about this, {lower}?',
                         'Would you like me to close this session?'],
        'clear_screen': ['This will most likely clear everything on the'
                         ' screen. Shall I do it?',
                         f'{title}, are you sure you want me to clear the'
                         ' screen?',
                         f'Are you sure about this, {lower}?',
                         f'Am I supposed to clear everything, {lower}?',
                         'Would you like me to clear everything on the'
                         ' screen?'],
        'user_command': [f'{title}, would you like to try your own commands?',
                         f'Are you sure about this, {lower}?',
                         'Custom commands requires confirmation. Are you sure'
                         ' about this?',
                         'Would you like me to start another terminal '
                         'session for you?'],
        'terminal_set': [f'The terminal is ready, {lower}.',
                         f'Your terminal is ready, {lower}.',
                         f'{title}, the terminal is ready. Please start'
                         ' typing.',
                         'Activating terminal... Ready'],
        'rename_model': [f'Would you like to rename the model, {lower}?'
                         f' Default model name is "{ai_lower}".',
                         f'Do you wish to rename the model, {lower}? Default'
                         f' model name is "{ai_lower}".',
                         f'Would you like to rename the model, {lower}?'
                         f' "{ai_lower}" is the default model name.',
                         f'Do you wish to rename the model, {lower}?'
                         f' "{ai_lower}" is the default model name.',
                         f'Would you like me to rename the model, {lower}?'
                         f' "{ai_lower}" is the default model name.']}
    # For handling errors.
    errors = {
        'no_internet': [f'{title}, it appears that we are not connected to'
                        ' the Internet. I am not able to perform the action.',
                        'We have no internet connection right now, I am not'
                        ' able to perform the action.',
                        f'Working on it, {lower}. It seems the internet'
                        ' connection is lost.',
                        f'{title}, currently there is no internet connection'
                        ' available.',
                        f'{title}, the internet connection is questionable.'
                        ' I am not able to perform the action.',
                        f'{title}, I am not able to access the internet.'],
        'unknown': [f'{title}, I\'m not able to perform this action. Perhaps'
                    ' could you please try that again?'
                    f' Sorry, {lower}. Perhaps could you rephrase that one'
                    ' more time, please?',
                    'I\'m afraid I didn\'t quite understand what you just'
                    ' said. Could you please repeat it one more time?',
                    'Pardon me, could you rephrase that one please?',
                    f'Pardon me, {lower}. Could you please rephrase that?'
                    f'My apologies, {lower}. But I\'m not able to perform'
                    ' that action. Perhaps could you try that again?']}
    # For handling weather related responses.
    weather_protocol = {
        'no_internet': [f'Internet connection is knackered, {lower}.',
                        f'Internet connection is not good, {lower}.',
                        f'Internet connection is questionable, {lower}.'],
        'saying_okay': [f'Okay, {lower}.',
                        f'Umm... okay, {lower}.',
                        'Okay.',
                        'On it.',
                        'Erm... okay.'],
        'working_on_it': ['Fetching weather details...',
                          'Working on it.',
                          'Just a moment...',
                          'Processing...',
                          'I\'m working on it...',
                          'Accessing weather details...'],
        'retrying': ['Not sure. I\'m working on it.',
                     'Trying again...',
                     'Retrying...'],
        'still_no_internet': [f'{title}, I\'m still not able to access the'
                              ' internet.',
                              'We still don\'t have a good internet'
                              ' connection.']}
except Exception as error:
    print('An error occured while performing this operation because of'
          f' {error} in function "{stack()[0][3]}" on line'
          f' {exc_info()[-1].tb_lineno}.')
