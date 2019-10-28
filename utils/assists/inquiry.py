"""
The inquiry module: Provides functions while inquiring on command line.

These functions are based of `questionary` module but provides more
custom use of the same. This module should be used on command line only
otherwise, it will raise an Exception.

At a glance, the structure of the module is following:
 - confirm():           Asks for confirmation. Provides Yes or No
                        options to confirm. It is recommended to use
                        this function by assigning it to a variable and
                        then the variable should be used in an if-else
                        condition to invoke the action.
 - answer():            Answers the asked question. It is recommended to
                        use this function while taking inputs.
 - secure():            This function is similar to the `answer`
                        function but instead of showing the value of the
                        input, it masks it with `*` just like the
                        password field in HTML/CSS.
 - decide():            Provides choice & then asks answer based on the
                        choosed option.
 - choose():            Provides options to choose from. These options
                        are then to be used for further code execution.
                        It is recommended to use this function when any
                        one of multiple options needs to be selected.
 - select_file():       Provides list of files to choose from directory.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.1 - Improved the type hints by using the typing module.
#           Made the code more* PEP-8 compliant.
#   1.0.2 - Synced all updates in history as other files.
#           Reduced unnecessary use of "`" in comments for simplicity.
#           Added new function, `select_file` to select a file from the
#           directory.
#   1.0.1 - Removed general questionary imports.
#           Added `choose` function to substitute the `select` from
#           questionary module and updated main docstring accordingly.
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info
from typing import List, Text, Union

# Constant used by `answer` and `decide` to return if no response is
# given.
_NO_RESPONSE = 'null'


def confirm(question: Text) -> bool:
    """Provides Yes or No options.

    question: Question for yes-no options.

    Asks for confirmation. Provides Yes or No options to confirm.

    Note: It is recommended to use this function by assigning it to a
    variable & then the variable should be used in an if-else condition
    to invoke the action.
    """
    from questionary import Choice, select

    return select(question, [Choice('Yes', True), Choice('No', False)]).ask()


def answer(question: Text) -> Text:
    """Takes input for question.

    question: Question that needs to be asked for expecting answer.

    Answers the asked question.

    Note: It is recommended to use this function while taking inputs.
    """
    from questionary import text

    try:
        # Asks question until it is responded with something.
        while True:
            revert = text(question + '\n»').ask()
            if revert == '':
                option = confirm(
                    'No inputs received. Would you like to try that again?')
                # Asks the same question again if a blank response is
                # given.
                while option is False:
                    # If no reply is to be given, it will return `null`
                    # as output of the `answer` function, else it will
                    # revert with given answer.
                    if option is False:
                        return _NO_RESPONSE
                    else:
                        revert = text(question + '\n»').ask()
                        return revert
            else:
                return revert
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def secure(question: Text) -> Text:
    """Takes input like password for question.

    question: Question that needs to be asked for expecting a secure
              answer.

    This function is similar to the `answer` function but instead of
    showing the value of the input, it masks it with `*` just like the
    password field in HTML/CSS.
    """
    from questionary import password

    try:
        # Similar to `answer` function, it asks question until it is
        # responded with something. Except here the input would be
        # masked with `*`.
        while True:
            revert = password(question + '\n»').ask()
            if revert == '':
                option = confirm(
                    'No inputs received. Would you like to try that again?')
                # Asks the same question again if a blank response is
                # given.
                while option is False:
                    # If no reply is to be given, it will return `null`
                    # as output of the `answer` function, else it will
                    # revert with given answer.
                    if option is False:
                        return _NO_RESPONSE
                    else:
                        revert = password(question + '\n»').ask()
                        return revert
            else:
                return revert
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def decide(confirm_question: Text, question: Text) -> Text:
    """Ask question if confirmed.

    confirm_question: Question that needs confirmation.
    question:         Question to be asked if confirmed.

    Provides choice and then asks answer based on the choosed option.
    """
    try:
        # Executes code if initial confirmation is asked.
        if confirm_question is not None:
            option = confirm(confirm_question)
            # If confirmed (said Yes) then ask next question.
            if option is True:
                revert = answer(question)
                return revert
            else:
                return _NO_RESPONSE
        else:
            return _NO_RESPONSE
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def choose(question: Text, **kwargs: Union[int, float, List, Text]) -> Text:
    """Provides options.

    question: Question or Message presenting multiple options.

    Provides options to choose from. These options are then to be used
    for further code execution.

    Note: It is recommended to use this function when any one of the
    multiple options needs to be selected.
    """
    from questionary import Choice, select

    return select(question, [Choice(v, k) for k, v in kwargs.items()]).ask()


def select_file(question: Text, file_dir: List) -> Text:
    """Provides list of files.

    question: Question or Message selecting multiple files.

    Provides option to select the file from a directory.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/questions/1747817/create-a-dictionary-with-list-comprehension
    from questionary import Choice, select

    files_dict = {index: file_dir[index] for index in range(0, len(file_dir))}
    return select(question,
                  [Choice(v, k) for k, v in files_dict.items()]).ask()
