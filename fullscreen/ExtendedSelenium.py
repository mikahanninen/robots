from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.base import keyword
from selenium.webdriver.common.keys import Keys
from enum import Enum





class ExtendedSelenium(Selenium):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @keyword
    def browser_zoomt(self, operating_system:str = "win", direction: str = "down"):
        modifier_key = Keys.CONTROL
        zoom_direction = "-"
        if operating_system == "mac":
            modifier_key = Keys.COMMAND
        if direction == "up":
            zoom_direction = "+"
        self.driver.set_context("chrome")
        body = self.driver.find_element_by_tag_name("html")
        body.send_keys(modifier_key, zoom_direction)
        self.driver.set_context("content")
        print(dir(self.driver))

