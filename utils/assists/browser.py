"""
The browser module: Provides functions related to Selenium.

This module will help you for browser based automation.

At a glance, the structure of the module is following:
 - wait_for_frame():    Explicitly waits till the frame is visible. The frame
                        can be any `frame` or `iframe` element. This function
                        uses the WebDriver instance and timeout in seconds.
                        Once the frame is detected, the wait stops and
                        execution is resumed.
 - find_class():        Explicitly waits till the particular class element is
                        detected in webcode. This function uses the WebDriver
                        instance and timeout in seconds. Once the class is
                        located, the wait stops and execution is resumed.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info
from time import sleep

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from charlotte.utils.assists.profile import lower, title
from charlotte.utils.paths.files import ai_file

# Constant used for declaring the path to chrome webdriver.
_CHROME_DRIVER_PATH = 'Z:/charlotte/charlotte/bin/chromedriver.exe'

options = ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--test-type')
# options.add_argument('--headless')
# options.add_argument('--incognito')
# options.add_argument('--start-maximized')
# options.add_argument('--start-minimized')
# options.add_argument('--disable-extensions')
# options.add_argument('--profile-directory=Default')
# options.add_argument('--disable-plugins-discovery')

try:
    # You can choose between various chrome options.
    chrome = Chrome(executable_path=_CHROME_DRIVER_PATH, options=options)
except Exception as error:
    print('An error occured while performing this operation because of'
          f' {error} in function "{stack()[0][3]}" on line'
          f' {exc_info()[-1].tb_lineno}.')
    chrome.quit()


def wait_for_frame(frame: str, time: int = 10) -> None:
    """Waits for frame.

    frame: Frame or IFrame to search on webpage.
    time:  Time to wait in secs.
           Default: 10 secs.

    Explicitly waits till the frame is visible. The frame can be any `frame`
    or `iframe` element. This function uses the WebDriver instance and timeout
    in seconds.

    Note: Once the frame is detected, the wait stops and the execution is
    resumed.
    """
    try:
        # WebDriver waiting instance till given time. Default wait time is 10s.
        wait = WebDriverWait(chrome, time)
        # Waits until the frame or iframe is visible in the webcode.
        wait.until(EC.frame_to_be_available_and_switch_to_it(frame))
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
        chrome.quit()


def find_class(class_name: str, time: int = 10) -> None:
    """Finds class.

    class_name: Name of the class to be searched on webpage.
    time:  Time to wait in secs.
           Default: 10 secs.

    Explicitly waits till the particular class element is detected in webcode.
    This function uses the WebDriver instance and timeout in seconds.

    Note: Once the class is located, the wait stops and execution is resumed.
    """
    try:
        # WebDriver waiting instance till given time. Default wait time is 10s.
        wait = WebDriverWait(chrome, time)
        # Waits until the class is located in the webcode.
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
        chrome.quit()
