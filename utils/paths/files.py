"""
This module provides references to all necessary files.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from charlotte.utils.paths.directories import ai_dir, local_dir, PARENT

ai_file = {
    'init': '__init__.py',
    'nlu': ai_dir['data']/'nlu.md',
    'core': ai_dir['data']/'stories.md',
    'master': ai_dir['users']/'master.yml',
    'actions': PARENT/'actions.py',
    'config': PARENT/'config.yml',
    'domain': PARENT/'domain.yml',
    'endpoints': PARENT/'endpoints.yml',
    'music': ai_dir['csv']/'music.csv'
}
