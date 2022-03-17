import logging
import os
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn


class CustomerLogging:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 2

    KEYWORDS_TO_FOLLOW = []

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.logger = logging.getLogger(__file__)
        self.logger.handlers = []
        self.log_next = None
        self.log_filename = Path(
            os.getenv("ROBOT_ARTIFACTS", os.curdir), "customer.log"
        )
        fileout = logging.FileHandler(filename=self.log_filename)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        fileout.setFormatter(formatter)
        self.logger.addHandler(fileout)

    def set_keywords_for_customer_log(self, keywords: list):
        self.KEYWORDS_TO_FOLLOW = keywords

    def customer_log(self, message: str):
        self.logger.info(message)

    def end_keyword(self, name, attributes):
        if attributes["kwname"] in self.KEYWORDS_TO_FOLLOW:
            self.log_next = attributes["kwname"]

    def log_message(self, message):
        if self.log_next:
            self.customer_log(f'{self.log_next}: {message["message"]}')
            self.log_next = None
