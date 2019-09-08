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
#   1.0.2 - Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from inspect import stack
from random import choice
from sys import exc_info

from charlotte.utils.actions.person import wish_user
from charlotte.utils.assists.profile import ai_lower, ai_title, lower, title

try:
    # All choices starting with `cmdline_main_options` are used by the run.py
    # module.
    cmdline_main_options_start_greet = choice([
        wish_user() + ' How can I assist you?',
        wish_user() + ' How can I help you?',
        wish_user() + ' What would you like me to do?',
        wish_user() + ' What can I help you with?',
        wish_user() + ' What can I do for you?',
        wish_user() + ' How may I help you?'])
    cmdline_main_options_model_choice = choice([
        'Which model you want to consider?',
        f'Which model, {lower}?',
        f'Alright. Which model, {lower}?',
        f'Which model you want to use, {lower}?'])
    cmdline_main_options_quit_confirm = choice([
        'Are you sure about leaving?',
        f'Are you sure, {lower}?',
        f'Shall I terminate this session, {lower}?',
        f'{title}, are you sure about this?',
        f'Are you sure about this, {lower}?',
        'Would you like me to close this session?'])
    cmdline_main_options_clear_screen = choice([
        'This will most likely clear everything on the screen. Shall I do it?',
        f'{title}, are you sure you want me to clear the screen?',
        f'Are you sure about this, {lower}?',
        f'Am I supposed to clear everything, {lower}?',
        'Would you like me to clear everything on the screen?'])
    cmdline_main_options_user_command = choice([
        f'{title}, would you like to try your own commands?',
        f'Are you sure about this, {lower}?',
        'Custom commands requires confirmation. Are you sure about this?',
        'Would you like me to start another terminal session for you?'])
    cmdline_main_options_terminal_set = choice([
        f'The terminal is ready, {lower}.',
        f'Your terminal is ready, {lower}.',
        f'{title}, the terminal is ready. Please start typing.',
        'Activating terminal... Ready'])
    # Choices starting with `rasa_model` are used by the rasa.py module.
    rasa_model_rename_check = choice([
        f'Would you like to rename the model, {lower}? Default model name '
        f'is "{ai_lower}".',
        f'Do you wish to rename the model, {lower}? Default model name '
        f'is "{ai_lower}".',
        f'Would you like to rename the model, {lower}? "{ai_lower}" is '
        'the default model name.',
        f'Do you wish to rename the model, {lower}? "{ai_lower}" is '
        'the default model name.',
        f'Would you like me to rename the model, {lower}? "{ai_lower}" is '
        'the default model name.'])
except Exception as error:
    print('An error occured while performing this operation because of'
          f' {error} in function "{stack()[0][3]}" on line'
          f' {exc_info()[-1].tb_lineno}.')
