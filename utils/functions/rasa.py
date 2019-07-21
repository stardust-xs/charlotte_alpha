"""
Charlotte` Rasa related functions
=================================

It stores all the functions needed for running Rasa over the CLI.

See https://github.com/xames3/charlotte for complete documentation.
"""
from __future__ import absolute_import
from __future__ import print_function

from os.path import exists
from subprocess import call
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from . basics import display, make_dir, model_check
from . questions import answer, confirm
from .. fluids.paths import DIR, FILE
from .. profile.user import ai_lower, ai_title, lower, title


def render_model(model: str = None) -> None:
    make_dir(DIR['models'])
    if model is None:
        option = confirm(
            f'Would you like to rename the model, {lower}? Default name is "{ai_lower}".')
        if option is True:
            model_name = answer(f'{title}, what would you like to call it?')
            call(
                f'rasa train --fixed-model-name "{model_name}" --force', shell=True)
        else:
            call(
                f'rasa train --fixed-model-name "{ai_lower}" --force', shell=True)
    else:
        option = confirm(
            f'Would you like to rename the model, {lower}? Default name is "{model}".')
        if option is True:
            model_name = answer(f'What would you like to call it, {lower}?')
            call(
                f'rasa train {model} --fixed-model-name "{model_name}" --force', shell=True)
        else:
            call(
                f'rasa train {model} --fixed-model-name "{model}" --force', shell=True)


def run_nlu():
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


def start_training():
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


def nlu_stats() -> list:
    """
    Definition
    ----------
        Returns all the intents and entities in NLU training data.
    """
    from rasa.nlu.training_data import load_data

    nlu_data = load_data(FILE['nlu'])
    intents = [nlu_data.intents]
    entities = [nlu_data.entities]
    return intents, entities
