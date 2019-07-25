"""
Charlotte Files
===============

This module provides references to all necessary files.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from charlotte.utils.paths.directories import ai_dir, PARENT

ai_file = {
    'init': '__init__.py',
    'key': ai_dir['cryptics']/'key.xai',
    'nlu': ai_dir['data']/'nlu.md',
    'core': ai_dir['data']/'stories.md',
    'master': ai_dir['users']/'master.yml',
    'actions': PARENT/'actions.py',
    'config': PARENT/'config.yml',
    'domain': PARENT/'domain.yml',
    'endpoints': PARENT/'endpoints.yml'
}
