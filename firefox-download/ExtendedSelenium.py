from cmath import exp
import os
from pathlib import Path
from time import sleep

from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.base import keyword
from selenium import webdriver
from webdrivermanager import GeckoDriverManager


class ExtendedSelenium(Selenium):
    def __init__(self, *args, **kwargs):
        self.download_dir = kwargs.pop("download_dir", ".")
        super().__init__(*args, **kwargs)

    @keyword
    def open_site(self, url, **kwargs):
        options = webdriver.FirefoxOptions()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference(
            "browser.download.dir", str(Path(self.download_dir).resolve())
        )
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.manager.focusWhenStarting", False)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        options.set_preference("browser.download.manager.alertOnEXEOpen", False)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.download.manager.closeWhenDone", True)
        options.set_preference("browser.download.viewableInternally.enabledTypes", "")
        options.set_preference("browser.helperApps.alwaysAsk.force", False)
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/pdf,text/plain,application/text,text/xml,application/xml,application/octet-stream",
        )
        options.set_preference("pdfjs.disabled", True)
        options.set_headless(True)

        self.open_browser(url=url, options=options, **kwargs)

    @keyword
    def firefox_download_and_wait_until_file_has_been_downloaded(
        self, locator: str, expected_filename: str
    ):
        self.click_element(locator)
        filename = expected_filename.rsplit("/")[-1]
        partial_filename = f"{filename}.part"
        while True:
            files = os.listdir(self.download_dir)
            if partial_filename in files:
                sleep(0.5)
                continue
            break
