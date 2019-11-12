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
                        use this function while taking inputs. If
                        `secure` arg is made True, it masks the response
                        with `*` just like the password field in HTML.
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
#   < Checkout my GitHub repo for history and latest stable build >
#
#   2.0.0 - Reworked script.
#           Merged `secure` function with `answer` function.
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

from typing import List, Optional, Text, Union

from questionary import Choice, select


def confirm(question: Text) -> bool:
    """Provides Yes or No options.

    question: Question for yes-no options.

    Asks for confirmation. Provides Yes or No options to confirm.

    Note: It is recommended to use this function by assigning it to a
    variable & then the variable should be used in an if-else condition
    to invoke the action.
    """
    return select(question, [Choice('Yes', True), Choice('No', False)]).ask()


def answer(question: Text, secure: Optional[bool] = False) -> Text:
    """Takes input for question.

    question: Question that needs to be asked for expecting answer.
    secure:   If True, it`ll mask the input and replace it with `*`.
              Default: False

    Answers the asked question. If `secure` arg is made True, it masks
    the response with `*` just like the password field in HTML.

    Note: It is recommended to use this function while taking inputs.
    """
    from questionary import password, text

    # Asks question until it is responded with something.
    question = question + '\n»'
    while True:
        revert = password(question).ask() if secure else text(question).ask()
        if revert == '':
            option = confirm(
                'No inputs received. Would you like to try that again?')
            # Asks the same question again if a blank response is given.
            while option is False:
                return None if option else revert
        else:
            return revert


def decide(confirm_question: Text,
           question: Text,
           secure: Optional[bool] = False) -> Text:
    """Ask question if confirmed.

    confirm_question: Question that needs confirmation.
    question:         Question to be asked if confirmed.
    secure:           If True, it masks the input & replace it with `*`.
                      Default: False

    Provides choice and then asks answer based on the choosed option.
    """
    option = confirm(confirm_question)
    return answer(question, secure) if option else None


def choose(question: Text, **kwargs: Union[int, float, List, Text]) -> Text:
    """Provides options.

    question: Question or Message presenting multiple options.

    Provides options to choose from. These options are then to be used
    for further code execution.

    Note: It is recommended to use this function when any one of the
    multiple options needs to be selected.
    """
    return select(question, [Choice(v, k) for k, v in kwargs.items()]).ask()


def select_file(question: Text, dir_name: List) -> Text:
    """Provides list of files.

    question: Question or Message selecting multiple files.
    dir_name: Directory from which the file needs to be chosen from.

    Provides option to select the file from a directory.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/questions/1747817/create-a-dictionary-
    # with-list-comprehension
    from os import listdir

    files = {index[0]: index[1] for index in enumerate(listdir(dir_name))}
    key = select(question, [Choice(v, k) for k, v in files.items()]).ask()
    return files[key]
