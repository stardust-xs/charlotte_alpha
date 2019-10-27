"""
The rasa module: Provides functions to use Rasa framework.

These functions help you perform tasks using the Rasa module with ease
and without re-writing them. It uses Rasa`s components to build, trains
and test the model.

At a glance, the structure of the module is following:
 - model_check():       Checks if the model exists in `./models/`
                        directory. It is recommended to use this
                        function while running model for testing and
                        during inference.
- render_model():       Creates models using your NLU data and stories.
                        The function renders model by overwriting the
                        previous model (if the model has same name).
                        This function trains a Rasa model that combines
                        Rasa NLU and Core models. If you only want to
                        choose specific model, you can use this function
                        to do so.
 - test_nlu():          Runs NLU test session for testing the model.
                        This function predicts the intent of given
                        statement and extracts the entities if present
                        in it. It will use the default Charlotte model,
                        `charlotte.tar.gz` for testing.
 - start_training():    Starts interactive learning session using
                        command, `rasa interactive`. It will use the
                        default Charlotte model, `charlotte.tar.gz` for
                        training. Training will be skipped if the
                        training data and config have not changed.
 - get_nlu_stats():     Creates a temporary file with all intents and
                        entities from the NLU data, `./data/nlu.md`
                        file. This values can be used for updating
                        intents and entities in the domain file. It is
                        recommended to use this function for checking
                        new intents & entities.
 - evaluate_model():    Evaluates quality of the model. The function
                        creates a timestamped folder within the
                        `./tests/` directory. It holds all the necessary
                        files related to the evaluation of the model.
                        It is recommended to use this function to check
                        the precision and accuracy of the model, if it
                        is overfitting or underfitting.

See https://github.com/xames3/charlotte for complete documentation.
"""
#   Still needed:
#       * Option to choose between multiple models in `test_nlu` func.
#
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.1 - Improved the type hints by using the typing module.
#           Made the code more* PEP-8 compliant.
#   1.1.0 - Added `make_dir` in `evaluate_model` function for creating
#           test directory.
#   1.0.6 - Updated comments in `render_model` function.
#           Updated command line comments to use new dictionaries from
#           phrases.py module.
#   1.0.3 - Added `show` warning in `render_model` function while
#           running the `rasa train` command.
#   1.0.2 - Added `show` in `get_nlu_stats` function to respond once the
#           temp result is generated.
#           Removed import `isfile` function import from general imports
#           as it is not used in any of the functions.
#           Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.1 - Added reference links to the functions.
#   1.0.0 - First code.

from __future__ import absolute_import
from __future__ import print_function

from inspect import stack
from random import choice
from subprocess import call
from sys import exc_info
from typing import NoReturn, Optional, Text

from charlotte.utils.assists.generic import make_dir, show, timestamp
from charlotte.utils.assists.inquiry import answer, confirm, choose
from charlotte.utils.assists.phrases import cmdline_options
from charlotte.utils.assists.profile import ai_lower, lower, title
from charlotte.utils.paths.directories import ai_dir
from charlotte.utils.paths.files import ai_file

# Constant used by `get_nlu_stats` to use default UTF-8 encoding.
_ENCODING = 'utf-8'


def model_check(model: Text,
                model_dir: Optional[Text] = ai_dir['models']) -> Text:
    """Checks if model exists.

    model:     Name of the model
    model_dir: Path of the models directory
               Default: `./models/`

    Checks if the model exists in `./models/` directory, and returns the
    model name.

    Note: It is recommended to use this function while running model for
    testing and during inference.
    """
    from os import walk
    from os.path import join

    try:
        for root, _, files in walk(model_dir):
            for file in files:
                # Checks if any file ending with `tar.gz` exists along
                # with given model name.
                if file.startswith(model.lower()) and file.endswith('tar.gz'):
                    return join(root, file)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def _build_domain() -> NoReturn:
    """Builds domain file.

    Updates domain file with my details.
    The function builds the domain file from the values which it imports
    from `./utils/assists/profile.py`.
    """
    from yaml import dump, load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    try:
        # Updates the primary username in the domain file before it
        # trains the model.
        domain = load(open(ai_file['domain']), Loader=Loader)
        domain['slots']['xa_lower']['initial_value'] = lower
        domain['slots']['xa_title']['initial_value'] = title
        with open(ai_file['domain'], 'w') as updated_domain:
            updated_domain.write(dump(domain, default_flow_style=False))
        # Replaces `null` with null, so that Rasa understands it while
        # using the domain file.
        with open(ai_file['domain'], 'r') as file_with_quoted_null:
            newlines = []
            for line in file_with_quoted_null.readlines():
                newlines.append(line.replace("'null'", 'null'))
        with open(ai_file['domain'], 'w') as file_without_quoted_null:
            for line in newlines:
                file_without_quoted_null.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def render_model() -> NoReturn:
    """Renders model.

    Creates models using your NLU data and stories. The function renders
    model by overwriting the previous model (if model has same name).

    Note: This function trains a Rasa model that combines Rasa NLU and
    Core models. If you only want to choose specific model, you can use
    this function to do so.
    """
    # You can find the reference code here:
    # https://rasa.com/docs/rasa/user-guide/command-line-interface/
    try:
        # Asks which model to render.
        type = choose(choice(cmdline_options['choose_model']),
                      nlu='NLU', core='Core', both='Both')
        # Builds domain file with the my details.
        _build_domain()
        make_dir(ai_dir['models'])
        rename = confirm(choice(cmdline_options['rename_model']))
        # If the model is to be renamed, it will take input and render
        # that model. Else, it will use `charlotte` as the default name.
        if rename is True:
            name = answer(f'{title}, what would you like to call it?').lower()
        else:
            name = ai_lower
            show('This will overwrite the existing main model.')
        # Appending model type to the name.
        if type == 'nlu':
            model = f'{type} --fixed-model-name "{name}_nlu"'
            call(f'rasa train {model}')
        elif type == 'core':
            model = f'{type} --fixed-model-name "{name}_core"'
            call(f'rasa train {model} --force --debug-plots --dump-stories')
        else:
            model = f'--fixed-model-name "{name}"'
            call(f'rasa train {model} --force --debug-plots --dump-stories')
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def test_nlu() -> NoReturn:
    """Tests NLU model.

    Runs NLU test session for testing the model. This function predicts
    the intent of given statement and extracts the entities if present
    in it.

    Note: It will use the default Charlotte model,
    `./models/charlotte.tar.gz` for testing.
    """
    # You can find the reference code here:
    # https://rasa.com/docs/rasa/user-guide/command-line-interface/
    try:
        # Checks if `charlotte.tar.gz` exists.
        if model_check(ai_lower):
            charlotte = model_check(ai_lower)
            call(f'rasa shell nlu model-as-positional-argument "{charlotte}"')
        else:
            # Renders the model if it does not exist.
            option = confirm(
                f'Sorry {lower}, I could not find NLU model in "./models/" '
                f'directory. Shall I create one now?')
            if option is True:
                render_model()
            else:
                show('Model not created.')
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def start_training() -> NoReturn:
    """Starts interactive learning session.

    Starts interactive learning using command, `rasa interactive`.

    Note: It will use the default Charlotte model,
    `./models/charlotte.tar.gz` for training. Training will be skipped
    if the training data and config have not changed.
    """
    # You can find the reference code here:
    # https://rasa.com/docs/rasa/user-guide/command-line-interface/
    try:
        # Checks if `charlotte.tar.gz` exists.
        # Story visualization is disabled as a personal preference. You
        # can enable it by removing `--skip-visualization` from the
        # below code.
        if model_check(ai_lower):
            charlotte = model_check(ai_lower)
            ep = ai_file['endpoints']
            call(f'rasa interactive --model {charlotte} --skip-visualization '
                 f'--endpoints {ep} --e2e --dump-stories')
        else:
            # Similar to `test_nlu` function, it renders the model if it
            # does not exist.
            option = confirm(
                f'Sorry {lower}, I could not find NLU model in "./models/" '
                f'directory. Shall I create one now?')
            if option is True:
                render_model()
            else:
                show('Model not created.')
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def get_nlu_stats() -> NoReturn:
    """Creates temporary file with NLU stats.

    Creates a temporary file with all intents and entities from the NLU
    data, `./data/nlu.md` file. This values can be used for updating
    intents and entities in the domain file.

    Note: It is recommended to use this function for checking new
    intents & entities.
    """
    from tempfile import TemporaryFile
    from rasa.nlu.training_data import load_data

    try:
        make_dir(ai_dir['temp'])
        # Loads NLU data from `./data/nlu.md` file.
        nlu_data = load_data(str(ai_file['nlu']))
        # Creates set of present intents and entities in the NLU data.
        intents = [nlu_data.intents][0]
        entities = [nlu_data.entities][0]
        # Creates a temporary file in `./temp/` directory.  The created
        # temporary file does not auto delete.
        named_temp_file = TemporaryFile(dir=ai_dir['temp'], delete=False)
        # Creates a list of all the intents and entities using the sets.
        with open(named_temp_file.name, 'w', encoding=_ENCODING) as temp_file:
            temp_file.write('Intents:\n')
            for index in intents:
                temp_file.write(index + '\n')
            temp_file.write('\nEntities:\n')
            for index in entities:
                temp_file.write(index + '\n')
        show(f'Done. Results are stored in {named_temp_file.name} file.')
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def evaluate_model() -> NoReturn:
    """Evaluates model.

    Evaluates quality of the model. The function creates a timestamped
    folder within the `./tests/` directory. It holds all the necessary
    files related to the evaluation of the model.

    Note: It is recommended to use this function to check the precision
    and accuracy of the model, if it is overfitting or underfitting.
    """
    # You can find the reference code here:
    # https://rasa.com/docs/rasa/user-guide/command-line-interface/
    from os.path import join

    try:
        make_dir(ai_dir['tests'])
        # Asks which model to evaluate.
        type = choose(choice(cmdline_options['choose_model']),
                      nlu='NLU', core='Core', both='Both')
        # Creates a folder within `./tests` directory with a timestamp.
        test_dir = join(ai_dir['tests'], timestamp('%d_%m_%Y_%I_%M_%S_%p'))
        make_dir(test_dir)
        type = '' if type == 'both' else type
        call(f'rasa test {type} --report {test_dir} --successes {test_dir}/'
             f'successes.json --errors {test_dir}/errors.json --histogram'
             f' {test_dir}/hist.png --confmat {test_dir}/confmat.png --cross'
             '-validation')
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
