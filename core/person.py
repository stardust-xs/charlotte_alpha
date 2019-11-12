"""
The person module: Provides functions related to the user.

These functions help to perform user level requests.

At a glance, the structure of the module is following:
 - greet_user():        Greets the user based on time of the day.
                        These responses needs to be expanded in future.
                        The greeting is returned on the basis of the
                        current hour.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   Still needed:
#       * Responses from `greet_user` function needs to be expanded.
#
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   2.0.0 - Reworked script.
#           Removed `age` & `locate` functions.
#           `greet_user` now returns just the greetings.
#   1.1.2 - Made the code more* PEP-8 compliant.
#           Profiled and optimized using `profiler`.
#           Improved the type hints by using the typing module.
#   1.0.6 - `greet_user` function now uses new dictionaries.
#   1.0.5 - `wish_user` is now changed to `greet_user` and fixed typos
#           in it.
#           `greet_user` function now returns time, hour & minutes.
#   1.0.4 - `locate` function now uses `check_internet` to check if
#           internet connection is available or not.
#   1.0.2 - Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from typing import Text

from charlotte.utils.constants import DARK, DAWN, DUSK, NOON
from charlotte.utils.phrases import greet


def greet_user() -> Text:
    """Greets user.

    Greets the user based on time of the day.

    Note: These responses needs to be expanded in future. The greeting
    is returned on the basis of the current hour.
    """
    from datetime import datetime
    from random import choice

    hour = datetime.now().hour
    morning = choice(greet['morning'])
    afternoon = choice(greet['afternoon'])
    evening = choice(greet['evening'])
    night = choice(greet['night'])
    # Determining which greeting should be used.
    greeting = morning if hour >= DAWN and hour < NOON else \
        afternoon if hour >= NOON and hour < DUSK else \
        evening if hour >= DUSK and hour < DARK else night
    # Returns greetings as per the day & current time-hour-minutes.
    return greeting
