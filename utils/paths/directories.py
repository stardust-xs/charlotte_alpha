"""
The directories module: Provides paths to all directories used in the package.

This module helps with the relative paths of the directories in this package.
It helps with overcoming the hassle of re-writing and hardcoding paths used for
reference.

At a glance, the structure of the module is following:
 - ai_dir{}:            Dictionary of all the important directories used in the
                        package.
 - local_dir{}:         Dictionary of all the directories in `D:/` drive.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.0 - First code.

from os.path import join
from pathlib import Path
from win32api import GetLogicalDriveStrings

PARENT = Path.cwd()


def _drives(drive_letter: str) -> str:
    """Returns drive letter.

    drive_letter: Drive letter to be searched for.

    Returns the drive letter from all the valid and present partitions. This
    assures that the user does not use any drive letter which is not present
    on the system.
    """
    partitions = GetLogicalDriveStrings().split('\000')[:-1]
    drive = {}
    try:
        for index in range(len(partitions)):
            keys = (Path(partitions[index]).parts[0].split(':\\')[0]).lower()
            values = partitions[index]
            drive[keys] = values
        return drive[drive_letter[0].lower()]
    except KeyError as error:
        missing_drive = str(error).strip('\'')
        print(f'Could not find {missing_drive.title()}:\\ drive.')


ai_dir = {
    'bin': PARENT/'bin/',
    'data': PARENT/'data/',
    'docs': PARENT/'docs',
    'logs': PARENT/'logs',
    'models': PARENT/'models',
    'temp': PARENT/'temp',
    'tests': PARENT/'tests',
    'utils': PARENT/'utils',
    'actions': PARENT/'utils/actions',
    'assists': PARENT/'utils/assists',
    'profiles': PARENT/'utils/profiles',
    'knowledge': PARENT/'data/knowledge',
    'csv': PARENT/'data/knowledge/csv'
}

local_dir = {
    'bittorrent': join(_drives('d'), 'Bittorrents'),
    'documents': join(_drives('d'), 'Documents'),
    'films': join(_drives('d'), 'Films'),
    'images': join(_drives('d'), 'Images'),
    'music': join(_drives('d'), 'Music'),
    'projects': join(_drives('d'), 'Projects'),
    'tutorials': join(_drives('d'), 'Tutorials'),
    'videos': join(_drives('d'), 'Videos'),
    'web_downloads': join(_drives('d'), 'Web Downloads')
}
