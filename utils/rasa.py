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

See https://github.com/xames3/charlotte for complete documentation.
"""
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   2.0.0 - Removed redundant functions.
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

from random import choice
from subprocess import call
from typing import NoReturn, Optional, Text

from charlotte.utils.inquiry import answer, choose, confirm
from charlotte.utils.generic import show
from charlotte.utils.paths import root, files
from charlotte.utils.phrases import NAME, TITLE, USER, cmd
from charlotte.utils.system import make_dir


def model_check(model: Text,
                dir_name: Optional[Text] = root['models']) -> Text:
    """Checks if model exists.

    model:     Name of the model
    dir_name:  Path of the models directory
               Default: `./models/`

    Checks if the model exists in `./models/` directory, and returns the
    model name.

    Note: It is recommended to use this function while running model for
    testing and during inference.
    """
    from os import listdir
    from os.path import join

    for file in listdir(dir_name):
        if file.startswith(model.lower()) and file.endswith('tar.gz'):
            return join(dir_name, file)


def build_domain() -> NoReturn:
    """Builds domain file.

    Updates domain file with my details.
    The function builds the domain file from the values which it imports
    from `./utils/constants.py`.
    """
    from yaml import dump, load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    # Updates username in the domain file before it trains the model.
    domain = load(open(files['domain']), Loader=Loader)
    domain['slots']['xa_lower']['initial_value'] = USER
    domain['slots']['xa_title']['initial_value'] = TITLE
    with open(files['domain'], 'w') as src_file:
        src_file.write(dump(domain, default_flow_style=False))
    # Replaces `null` with null using the domain file.
    with open(files['domain'], 'r') as src_file:
        new = [line.replace("'null'", 'null') for line in src_file.readlines()]
    with open(files['domain'], 'w') as src_file:
        src_file.writelines(new)


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
    # Asks which model to render.
    type = choose(choice(cmd['choose']), nlu='NLU', core='Core', both='Both')
    # Builds domain file with the my details.
    build_domain()
    make_dir(root['models'])
    rename = confirm(choice(cmd['rename']))
    name = answer('What would you like to call it?') if rename else NAME
    # Appending model type to the name.
    if type == 'nlu':
        model = f'{type} --fixed-model-name "{name.lower()}_nlu"'
        call(f'rasa train {model}')
    elif type == 'core':
        model = f'{type} --fixed-model-name "{name.lower()}_core"'
        call(f'rasa train {model} --force')
    else:
        model = f'--fixed-model-name "{name.lower()}"'
        call(f'rasa train {model} --force')


def start_training() -> NoReturn:
    """Starts interactive learning session.

    Starts interactive learning using command, `rasa interactive`.

    Note: It will use the default Charlotte model,
    `./models/charlotte.tar.gz` for training. Training will be skipped
    if the training data and config have not changed.
    """
    # You can find the reference code here:
    # https://rasa.com/docs/rasa/user-guide/command-line-interface/
    if model_check(NAME):
        charlotte = model_check(NAME)
        endpoints = files['endpoints']
        call(f'rasa interactive --model {charlotte} --skip-visualization '
             f'--endpoints {endpoints} --e2e')
    else:
        # It renders the model if it does not exist.
        option = confirm(f'Sorry {USER}, I could not find NLU model in '
                         '"./models/" directory. Shall I create one now?')
        if option is True:
            render_model()
        else:
            show('Model not created.')


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
    from charlotte.utils.constants import ENCODING

    make_dir(root['temp'])
    # Loads NLU data from `./data/nlu.md` file.
    nlu_data = load_data(str(files['nlu']))
    # Creates set of present intents and entities in the NLU data.
    intents = [nlu_data.intents][0]
    entities = [nlu_data.entities][0]
    # Creates a temporary file in `./files/temp/` directory.
    # The created temporary file does not auto delete.
    named_temp_file = TemporaryFile(dir=root['temp'], delete=False)
    # Creates a list of all the intents and entities using the sets.
    with open(named_temp_file.name, 'w', encoding=ENCODING) as temp_file:
        temp_file.write('Intents:\n')
        for index in intents:
            temp_file.write(index + '\n')
        temp_file.write('\nEntities:\n')
        for index in entities:
            temp_file.write(index + '\n')
    show(f'Done. Results are stored in {named_temp_file.name} file.')
