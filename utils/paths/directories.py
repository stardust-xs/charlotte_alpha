"""
The directories module: Provides paths to all directories used in the
package.

This module helps with the relative paths of the directories in this
package. It helps with overcoming the hassle of re-writing & hardcoding
paths used for reference.

At a glance, the structure of the module is following:
 - ai_dir{}:            Dictionary of all the important directories used
                        in the package.
 - local_dir{}:         Dictionary of all directories in `D:/` drive.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.1 - Improved the type hints by using the typing module.
#           Made the code more* PEP-8 compliant.
#           Updated paths as per new configuration.
#   1.1.0 - Stories are now part of `./data/stories/` directory.
#   1.0.0 - First code.

from os.path import join
from pathlib import Path
from typing import Text
from win32api import GetLogicalDriveStrings

PARENT = Path.cwd()


def _drives(drive_letter: Text) -> Text:
    """Returns drive letter.

    drive_letter: Drive letter to be searched for.

    Returns the drive letter from all the valid and present partitions.
    This assures that the user does not use any drive letter which is
    not present on the system.
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
    'data': PARENT/'data/',
    'logs': PARENT/'logs',
    'models': PARENT/'models',
    'backup': PARENT/'backup',
    'temp': PARENT/'temp',
    'tests': PARENT/'tests',
    'utils': PARENT/'utils',
    'actions': PARENT/'utils/actions',
    'assists': PARENT/'utils/assists',
    'knowledge': PARENT/'data/knowledge',
    'stories': PARENT/'data/stories',
    'csv': PARENT/'data/knowledge/csv'
}

local_dir = {
    'bittorrent': join(_drives('d'), 'Bittorrents'),
    'documents': join(_drives('d'), 'Documents'),
    'films': join(_drives('d'), 'Films'),
    'photos': join(_drives('d'), 'Photos'),
    'music': join(_drives('d'), 'Music'),
    'xa': join(_drives('d'), 'XA'),
    'videos': join(_drives('d'), 'Videos'),
    'web': join(_drives('d'), 'Web')
}
