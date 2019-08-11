"""
Charlotte Rasa Functions
========================

This module provides reference to Rasa NLP toolkit.
The module uses Rasa`s components and builds models, trains the model and
test the model.
The module has 5 functions:
    - domain_builder    : Updates domain file with user details
    - render_model      : Create models
    - run_nlu           : Runs NLU shell
    - start_training    : Starts Interactive Training process
    - nlu_stats         : Provides NLU statistics

See https://github.com/xames3/charlotte for complete documentation.
"""
from __future__ import absolute_import
from __future__ import print_function

from os.path import exists
from subprocess import call

from charlotte.utils.helpers.common import display, make_dir, model_check
from charlotte.utils.helpers.questions import answer, confirm
from charlotte.utils.paths.directories import ai_dir
from charlotte.utils.paths.files import ai_file
from charlotte.utils.profiles.user import ai_lower, lower, title


def domain_builder() -> None:
    """
    Definition
    ----------
        Builds domain file with user details.

    Notes
    -----
        The function builds the domain file from the values
        which it imports from `./utils/profiles/user.py`.
    """
    from yaml import dump, load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    try:
        domain = load(open(ai_file['domain']), Loader=Loader)
        domain['slots']['xa']['initial_value'] = title

        with open(ai_file['domain'], 'w') as updated_domain:
            updated_domain.write(dump(domain, default_flow_style=False))
        with open(ai_file['domain'], 'r') as file_with_quoted_null:
            newlines = []
            for line in file_with_quoted_null.readlines():
                newlines.append(line.replace("'null'", 'null'))
        with open(ai_file['domain'], 'w') as file_without_quoted_null:
            for line in newlines:
                file_without_quoted_null.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def render_model(model: str = None) -> None:
    """
    Definition
    ----------
        Renders model using command, `rasa train --fixed-model-name "<model>"`

    Parameter
    ---------
        model : string, optional
            Model to be created.
            Global default: charlotte

    Notes
    -----
        Function renders model by overwriting the previous model (if the model
        has same name).
    """
    try:
        domain_builder()
        make_dir(ai_dir['models'], need_init=False)
        if model is None:
            option = confirm(
                f'Would you like to rename the model, {lower}? Default name is "{ai_lower}".')
            if option is True:
                model_name = answer(
                    f'{title}, what would you like to call it?')
                call(
                    f'rasa train --fixed-model-name "{model_name}" --force', shell=True)
            else:
                call(
                    f'rasa train --fixed-model-name "{ai_lower}" --force', shell=True)
        else:
            option = confirm(
                f'Would you like to rename the model, {lower}? Default name is "{model}".')
            if option is True:
                model_name = answer(
                    f'What would you like to call it, {lower}?')
                call(
                    f'rasa train {model} --fixed-model-name "{model_name}" --force', shell=True)
            else:
                call(
                    f'rasa train {model} --fixed-model-name "{model}" --force', shell=True)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def run_nlu() -> None:
    """
    Definition
    ----------
        Tests NLU model using command, `rasa shell nlu`.

    Notes
    -----
        It will use the default Charlotte model, `./models/charlotte.tar.gz`
    """
    try:
        if model_check(ai_lower):
            charlotte = model_check(ai_lower)
            call(
                f'rasa shell nlu model-as-positional-argument "{charlotte}"', shell=True)
        else:
            option = confirm(
                f'Sorry {lower}, I couldn\'t find NLU model in ./models directory. Shall I create one now?')
            if option is True:
                render_model()
            else:
                display('Model not created.')
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def start_ai_training() -> None:
    """
    Definition
    ----------
        Starts an Interactive Training session using command, `rasa
        interactive`

    Notes
    -----
        It will use the default Charlotte model, `./models/charlotte.tar.gz`
    """
    try:
        if model_check(ai_lower):
            charlotte = model_check(ai_lower)
            call(
                f'rasa interactive --model {charlotte} --skip-visualization', shell=True)
        else:
            option = confirm(
                f'Sorry {lower}, I couldn\'t find my model in ./models directory. Shall I create one now?')
            if option is True:
                render_model()
            else:
                display('Model not created.')
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def nlu_stats() -> list:
    """
    Definition
    ----------
        Returns all the intents and entities in NLU training data.
        This values can be used for adding the intents and entities in the
        domain file.
    """
    from rasa.nlu.training_data import load_data

    try:
        nlu_data = load_data(str(ai_file['nlu']))
        intents = [nlu_data.intents]
        entities = [nlu_data.entities]
        return intents, entities
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')
