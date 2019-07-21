"""
Charlotte`s paths
=================

It contains paths to accessing directories and files.

See https://github.com/xames3/charlotte for complete documentation.
"""
from os.path import dirname, join

PARENT = dirname(dirname(dirname(__file__)))

DIR = {
    'data': join(PARENT, 'data/'),
    'docs': join(PARENT, 'docs/'),
    'logs': join(PARENT, 'logs/'),
    'models': join(PARENT, 'models/'),
    'users': join(PARENT, 'users/'),
    'utils': join(PARENT, 'utils/'),
    'fluids': join(PARENT, 'utils/fluids/'),
    'functions': join(PARENT, 'utils/functions/'),
    'profile': join(PARENT, 'utils/profile/'),
    'security': join(PARENT, 'utils/security/')
}

FILE = {
    'init': '__init__.py',
    'nlu': join(DIR['data'], 'nlu.md'),
    'core': join(DIR['data'], 'stories.md'),
    'actions': join(PARENT, 'actions.py'),
    'config': join(PARENT, 'config.yml'),
    'domain': join(PARENT, 'domain.yml'),
    'endpoints': join(PARENT, 'endpoints.yml'),
    'master': join(DIR['users'], 'master.yml'),
    'key': join(DIR['security'], 'key.xai')
}

DRIVE = {
    'c': 'C:/',
    'd': 'D:/',
    'e': 'E:/',
    'f': 'F:/',
    'k': 'K:/',
    'z': 'Z:/',
}

PATH = {
    'bittorrent': join(DRIVE['d'], 'Bittorrents'),
    'documents': join(DRIVE['d'], 'Documents'),
    'films': join(DRIVE['d'], 'Films'),
    'images': join(DRIVE['d'], 'Images'),
    'music': join(DRIVE['d'], 'Music'),
    'projects': join(DRIVE['d'], 'Projects'),
    'tutorials': join(DRIVE['d'], 'Tutorials'),
    'videos': join(DRIVE['d'], 'Videos'),
    'web_downloads': join(DRIVE['d'], 'Web Downloads')
}
