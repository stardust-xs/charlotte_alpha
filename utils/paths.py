"""
The paths module: Provides paths to all directories & files used in the
project.

This module helps with the relative paths of the directories as well as
the files used in this project. It helps with overcoming the hassle of
re-writing & hardcoding paths used for reference.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   2.0.0 - Merged directories.py and files.py into single file.
#           Removed "_drives" function and moved it to system module.
#   1.1.1 - Improved the type hints by using the typing module.
#           Made the code more* PEP-8 compliant.
#           Updated paths as per new configuration.
#   1.1.0 - Stories are now part of `./data/stories/` directory.
#   1.0.0 - First code.

from pathlib import Path

PARENT = Path.cwd()

root = {
    'cache': PARENT/'cache/',
    'core': PARENT/'core/',
    'data': PARENT/'data/',
    'stories': PARENT/'data/stories/',
    'lookups': PARENT/'data/lookups/',
    'database': PARENT/'database/',
    'experimental': PARENT/'experimental/',
    'files': PARENT/'files/',
    'temp': PARENT/'files/temp/',
    'models': PARENT/'models/',
    'saved_models': PARENT/'models/saved_models/',
    'utils': PARENT/'utils/',
    'website': PARENT/'website/',
}

files = {
    'init': '__init__.py',
    'nlu': root['data']/'nlu.md',
    'config': PARENT/'config.yml',
    'credentials': PARENT/'credentials.yml',
    'domain': PARENT/'domain.yml',
    'endpoints': PARENT/'endpoints.yml',
}
