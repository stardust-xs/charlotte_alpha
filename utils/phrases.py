"""
The phrases module: Replies with responses at inference.

This module is built for returning replies for particular task.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   2.0.0 - Reworked script.
#   1.1.2 - Added example value to `yes_boss` key.
#   1.1.1 - Made the code more* PEP-8 compliant.
#   1.1.0 - Changed all variables into dictionary values.
#   1.0.7 - Added one more phrase in weather_protocol[`retrying`].
#   1.0.6 - Replaced all options into respective dictionaries for better
#           handling.
#   1.0.5 - Updated `wish_user` to `greet_user`.
#   1.0.4 - Added one example to `no_internet_connection` and fixed typo
#           in it.
#   1.0.3 - Added new phrase option, `no_internet_connection`.
#   1.0.2 - Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from charlotte.utils.constants import NAME, USER

TITLE = USER.capitalize()

# For command line.
cmd = {
    'greet': ['How can I assist you?', 'How can I help you?',
              'What would you like me to do?', 'What can I help you with?',
              'What can I do for you?', 'How may I help you?'],
    'choose': ['Which model you want to consider?',
               f'Which model, {USER}?',
               f'Alright. Which model, {USER}?',
               f'Which model you want to use, {USER}?'],
    'quit': ['Are you sure about leaving?',
             f'Are you sure, {USER}?',
             f'Shall I terminate this session, {USER}?',
             f'{TITLE}, are you sure about this?',
             f'Are you sure about this, {USER}?',
             'Would you like me to close this session?'],
    'clear': ['This will clear everything on the screen. Shall I do it?',
              f'{TITLE}, are you sure you want me to clear the screen?',
              f'Are you sure about this, {USER}?',
              f'Am I supposed to clear everything, {USER}?',
              'Would you like me to clear everything on the screen?'],
    'custom': [f'Are you sure about this, {USER}?',
               'Custom commands requires confirmation. Are you sure about '
               'this?',
               'Would you like me to start another terminal session for you?'],
    'ready': [f'The terminal is ready, {USER}.',
              f'Your terminal is ready, {USER}.',
              f'{TITLE}, the terminal\'s ready. Please start typing.',
              'Activating terminal... Ready'],
    'rename': [f'Would you like to rename the model, {USER}?'
               f' Default model name is "{NAME}".',
               f'Do you wish to rename the model, {USER}? Default'
               f' model name is "{NAME}".',
               f'Would you like to rename the model, {USER}?'
               f' "{NAME}" is the default model name.']}

# For greeting the user.
greet = {
    'morning': [f'Good Morning, {TITLE}.', 'Good Morning!'],
    'afternoon': [f'Good Afternoon, {TITLE}.', 'Good Afternoon!'],
    'evening': [f'Good Evening, {TITLE}.', 'Good Evening!'],
    'night': [f'Hello, {TITLE}!', f'Welcome back, {TITLE}.'],
    'ready': [f'{TITLE}?', f'Yes, {USER}?', 'Yes?']}

# For handling errors.
errors = {
    'no_internet': [f'{TITLE}, it appears that we are not connected to'
                    ' the Internet. I\'m not able to perform the action.',
                    'We have no internet connection right now, I\'m not'
                    ' able to perform the action.',
                    f'Working on it, {USER}. It seems the internet'
                    ' connection is lost.',
                    f'{TITLE}, currently there is no internet connection'
                    ' available.',
                    f'{TITLE}, the internet connection is questionable.'
                    ' I\'m not able to perform the action.',
                    f'{TITLE}, I\'m not able to access the internet.'],
    'unknown': [f'{TITLE}, I\'m not able to perform this action. Perhaps'
                ' could you please try that again?'
                f' Sorry, {USER}. Perhaps could you rephrase that one'
                ' more time, please?',
                'I\'m afraid I didn\'t quite understand what you just'
                ' said. Could you please repeat it one more time?',
                'Pardon me, could you rephrase that one please?',
                f'Pardon me, {USER}. Could you please rephrase that?'
                f'My apologies, {USER}. But I\'m not able to perform'
                ' that action. Perhaps could you try that again?']}

# For handling weather related responses.
weather = {
    'no_internet': [f'Internet connection is knackered, {USER}.',
                    f'Internet connection is not good, {USER}.',
                    f'Internet connection is questionable, {USER}.'],
    'okay': [f'Okay, {USER}.', f'Umm... okay, {USER}.', 'Okay.', 'On it.',
             'Erm... okay.'],
    'wait': ['Fetching weather details...', 'Working on it.',
             'Just a moment...', 'Processing...', 'I\'m working on it...',
             'Accessing weather details...'],
    'retry': ['Not sure. I\'m working on it.', 'Trying again...',
              'Retrying...'],
    'still': [f'{TITLE}, I\'m still not able to access the  internet.',
              f'We still don\'t have an active internet connection, {USER}.']}
