"""
The run module: Runs Charlotte on terminal.

This is the main module. It enables to operate and perform Charlotte`s actions.

At a glance, the structure of the module is following:
 - render_model:        Renders the model by giving choices between NLU, Core
                        or Both options.
 - start_training:      Starts interactive learning session.
 - evaluate_model:      Evaluates the model by giving choices between NLU, Core
                        or Both options.
 - test_nlu:            Starts NLU testing session.
 - get_nlu_stats:       Creates temporary file with NLU statistics.
 - start_action_server: Starts Action server for running custom actions.
 - user_command:        Enables running of custom commands.
 - clear_screen:        Clears everything on terminal.
 - exit:                Terminates the session.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.3 - Deprecated `select` and used `choose` instead.
#   1.0.0 - First code.

from inspect import stack
from subprocess import call
from sys import exc_info, exit

from charlotte.utils.assists.inquiry import answer, choose, confirm
from charlotte.utils.assists.phrases import (cmdline_main_options_start_greet,
                                             cmdline_main_options_quit_confirm,
                                             cmdline_main_options_clear_screen,
                                             cmdline_main_options_user_command,
                                             cmdline_main_options_terminal_set)
from charlotte.utils.assists.rasa import (evaluate_model,
                                          get_nlu_stats,
                                          render_model,
                                          start_training,
                                          test_nlu)
from charlotte.utils.assists.constants import ACTION_SERVER_PORT

try:
    while True:
        option = choose(cmdline_main_options_start_greet,
                        render_model='Render model',
                        start_training='Train system',
                        evaluate_model='Evaluate model',
                        test_nlu='Test NLU model',
                        get_nlu_stats='Get NLU statistics',
                        start_action_server='Start Action Server',
                        user_command='Run user commands',
                        clear_screen='Clear screen',
                        exit='Exit')
        if option is 'render_model':
            render_model()
        elif option is 'start_training':
            start_training()
        elif option is 'evaluate_model':
            evaluate_model()
        elif option is 'test_nlu':
            test_nlu()
        elif option is 'get_nlu_stats':
            get_nlu_stats()
        elif option is 'start_action_server':
            call(f'rasa run actions -p {ACTION_SERVER_PORT}', shell=True)
        elif option is 'user_command':
            option = confirm(cmdline_main_options_user_command)
            if option is True:
                call(answer(cmdline_main_options_terminal_set), shell=True)
        elif option is 'clear_screen':
            option = confirm(cmdline_main_options_clear_screen)
            if option is True:
                call('cls', shell=True)
        elif option is 'exit':
            option = confirm(cmdline_main_options_quit_confirm)
            if option is True:
                exit()
except Exception as error:
    print('An error occurred while performing this operation because of'
          f' {error} in function "{stack()[0][3]}" on line'
          f' {exc_info()[-1].tb_lineno}.')
