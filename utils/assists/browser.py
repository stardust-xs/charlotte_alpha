"""
This module hosts functions related to Selenium which inherently helps for
browser based automation.

See https://github.com/xames3/charlotte for cloning the repository.
"""
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

from charlotte.utils.paths.files import ai_file
from charlotte.utils.profiles.default import lower, title

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
    chrome = Chrome(executable_path=r'Z:\charlotte\charlotte\bin\chromedriver.exe',
                    options=options)
except Exception as error:
    print('An error occured while performing this operation because of'
          f' {error} in function "{stack()[0][3]}" on line'
          f' {exc_info()[-1].tb_lineno}.')
    chrome.quit()


def wait_visible_frame(frame: str, time: int = 10) -> None:
    """
    Definition
    ----------
        Waits until a frame is visible on the webpage.

    Parameters
    ----------
        frame : string, mandatory
            Frame to search on webpage.

        time : integer, mandatory
            Time to wait in secs.
            Global default: 10 secs.
    """
    try:
        wait = WebDriverWait(chrome, time)
        wait.until(EC.frame_to_be_available_and_switch_to_it(frame))
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
        chrome.quit()


def find_class(class_name: str, time: int = 10) -> None:
    try:
        wait = WebDriverWait(chrome, time)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
        chrome.quit()
