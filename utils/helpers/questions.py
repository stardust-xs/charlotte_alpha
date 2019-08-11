"""
Charlotte Question Functions
============================

This module references functions that are used while interacting on Command
Line Interface.
The module has 4 functions:
    - confirm       : Asks for confirmation
    - answer        : Answers a question
    - secure        : Answers question as a password
    - decide        : Confirms the condition and asks question

See https://github.com/xames3/charlotte for cloning the repository.
"""
from questionary import Choice, select, text, password


def confirm(question: str) -> bool:
    """
    Definition
    ----------
        Provides `Yes` or `No` options for the user to confirm.

    Parameter
    ---------
        question : string, mandatory
            String that needs to be displayed as message OR a question for the
            below choices.

    Returns
    -------
        option : string, default
            Returns `yes` or `no`.

    Notes
    -----
        This function needs to be assigned to a variable and then the variable
        should be used in an `if-else` condition to invoke the action.
    """
    return select(message=question,
                  choices=[Choice('Yes', True),
                           Choice('No', False)]).ask()


def answer(question: str) -> str:
    """
    Definition
    ----------
        Answers to the asked question.

    Parameter
    ---------
        question : string, mandatory
            Question that needs to be asked for expecting answer.

    Returns
    -------
        revert : string, default
            Returns one-word* answer to the question.

    Notes
    -----
        This function needs to be assigned to a variable and then the variable
        should be used in an `if-else` condition to invoke the action.
    """
    try:
        while True:
            revert = text(question + '\n»').ask()
            if revert is '':
                option = confirm(
                    'No inputs received. Would you like to try that again?')
                while option is False:
                    if option is False:
                        return 'null'
                    else:
                        revert = text(question + '\n»').ask()
                        return revert
            else:
                return revert
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def secure(question: str) -> str:
    """
    Definition
    ----------
        Answers securely to the asked question.

    Parameter
    ---------
        question : string, mandatory
            Question that needs to be asked for expecting answer. The function
            will treat answer like password, concealing the output using `*`.

    Returns
    -------
        revert : string, default
            Returns one-word* answer to the question with `*`.

    Notes
    -----
        This function displays output in terms of `*` while returning it in
        it`s true form.
    """
    try:
        while True:
            revert = password(question + '\n»').ask()
            if revert is '':
                option = confirm(
                    'No inputs received. Would you like to try that again?')
                while option is False:
                    if option is False:
                        return 'null'
                    else:
                        revert = password(question + '\n»').ask()
                        return revert
            else:
                return revert
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def decide(confirm_question: str, question: str) -> str:
    """
    Definition
    ----------
        Provides choice and asks answer based on the choosed option.

    Parameters
    ----------
        Question that needs to be asked for expecting answer if the user has
        opinions.

    Returns
    -------
        revert : string, default
            Answers the question based on chosed option.
    """
    try:
        if confirm_question is not None:
            option = confirm(confirm_question)
            if option is True:
                revert = answer(question)
                return revert
            else:
                return 'null'
        else:
            return 'null'
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')
