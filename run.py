"""
Charlotte Console
=================

This module runs Charlotte on terminal.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exit
from subprocess import call

from questionary import Choice, select

from charlotte.utils.helpers.common import display
from charlotte.utils.helpers.questions import answer, confirm
from charlotte.utils.profiles.user import ai_lower, ai_title, lower, title
from charlotte.utils.helpers.rasa import (render_model,
                                          run_nlu,
                                          start_training)

while True:
    option = select(message=f'Hello {lower}, what would you like me to do?',
                    choices=[Choice('Render model', 'render_model'),
                             Choice('Start training', 'start_training'),
                             Choice('Test NLU model', 'run_nlu'),
                             Choice('Run custom commands', 'custom_commands'),
                             Choice('Clear screen', 'clear_screen'),
                             Choice('Exit', 'exit')]).ask()

    if option is 'render_model':
        render_model()
    elif option is 'start_training':
        start_training()
    elif option is 'run_nlu':
        run_nlu()
    elif option is 'custom_commands':
        option = confirm(f'{title}, would you like to try your own commands?')
        if option is True:
            custom_command = answer(
                f'The terminal is ready, {lower}. Start typing.')
            call(custom_command, shell=True)
    elif option is 'clear_screen':
        option = confirm(f'{title}, do you want me to clear the screen?')
        if option is True:
            call('cls', shell=True)
    elif option is 'exit':
        option = confirm(f'Are you sure, {lower}?')
        if option is True:
            exit()
