import logging
import os
from pathlib import Path


class CustomerLogging:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 2

    KEYWORDS_TO_FOLLOW = []
    MESSAGES_TO_FOLLOW = []

    def __init__(self, log_filename: str = None, date_format: str = None):
        self.ROBOT_LIBRARY_LISTENER = self
        self.logger = logging.getLogger(__file__)
        self.logger.handlers = []
        log_filename = (
            Path(log_filename)
            if log_filename
            else Path(os.getenv("ROBOT_ARTIFACTS", os.curdir), "customer.log")
        )
        log_filename.parent.mkdir(parents=True, exist_ok=True)
        self.log_filename = log_filename
        fileout = logging.FileHandler(filename=self.log_filename)
        kwargs = {}
        if date_format:
            kwargs["datefmt"] = date_format
        formatter = logging.Formatter("%(asctime)s - %(message)s", **kwargs)
        fileout.setFormatter(formatter)
        self.logger.addHandler(fileout)

    def set_keywords_for_customer_log(self, keywords: list):
        self.KEYWORDS_TO_FOLLOW = keywords

    def set_messages_for_customer_log(self, messages: list):
        self.MESSAGES_TO_FOLLOW = messages

    def customer_log(self, message: str):
        self.logger.info(message)

    def end_keyword(self, name, attributes):
        if attributes["kwname"] in self.KEYWORDS_TO_FOLLOW:
            self.customer_log(
                f'{attributes["kwname"]} called with arguments: {",".join(attributes["args"])}'
            )

    def log_message(self, message):
        matches = [
            msg.lower() in message["message"].lower() for msg in self.MESSAGES_TO_FOLLOW
        ]
        if any(matches):
            self.customer_log(message["message"])
