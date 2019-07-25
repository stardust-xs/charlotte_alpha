"""
Charlotte Directories
=====================

This module provides references to all directories.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from os.path import join
from pathlib import Path
from win32api import GetLogicalDriveStrings


def drives(drive_letter: str) -> str:
    partitions = GetLogicalDriveStrings().split('\000')[:-1]
    drive = {}
    try:
        for index in range(len(partitions)):
            keys = (Path(partitions[index]).parts[0].split(':\\')[0]).lower()
            values = partitions[index]
            drive[keys] = values
        return drive[drive_letter]
    except KeyError as error:
        missing_drive = str(error).strip('\'')
        print(f'Couldn\'t find {missing_drive.title()}:\\ drive')


PARENT = Path.cwd()

ai_dir = {
    'data': PARENT/'data/',
    'docs': PARENT/'docs',
    'logs': PARENT/'logs',
    'models': PARENT/'models',
    'users': PARENT/'users',
    'utils': PARENT/'utils',
    'cryptics': PARENT/'utils/cryptics',
    'globals': PARENT/'utils/globals',
    'helpers': PARENT/'utils/helpers',
    'profiles': PARENT/'utils/profiles'
}

local_dir = {
    'bittorrent': join(drives('d'), 'Bittorrents'),
    'documents': join(drives('d'), 'Documents'),
    'films': join(drives('d'), 'Films'),
    'images': join(drives('d'), 'Images'),
    'music': join(drives('d'), 'Music'),
    'projects': join(drives('d'), 'Projects'),
    'tutorials': join(drives('d'), 'Tutorials'),
    'videos': join(drives('d'), 'Videos'),
    'web_downloads': join(drives('d'), 'Web Downloads')
}
