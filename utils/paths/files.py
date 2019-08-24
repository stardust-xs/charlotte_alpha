"""
This module provides references to all necessary files.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from charlotte.utils.paths.directories import ai_dir, local_dir, PARENT

ai_file = {
    'init': '__init__.py',
    'nlu': ai_dir['data']/'nlu.md',
    'core': ai_dir['data']/'stories.md',
    'actions': PARENT/'actions.py',
    'config': PARENT/'config.yml',
    'domain': PARENT/'domain.yml',
    'endpoints': PARENT/'endpoints.yml',
    'chrome': ai_dir['bin']/'chromedriver.exe',
    'music': ai_dir['csv']/'music.csv'
}
