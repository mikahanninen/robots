from RPA.core.windows.locators import Locator, WindowsElement
from RPA.Windows import Windows
from RPA.Windows import utils
from RPA.Windows.keywords import keyword
from RPA.Windows.keywords.context import ActionNotPossible
from typing import Optional

if utils.IS_WINDOWS:
    import uiautomation as auto


def get_raw_keys(keys):
    raw_text = ""
    for k in keys:
        if k == "{":
            raw_text += "{{}"
        elif k == "}":
            raw_text += "{}}"
        else:
            raw_text += k
    return raw_text


class ExtendedWindows(Windows):
    def __init__(self, *args, **kwargs):
        Windows.__init__(self, *args, **kwargs)

    @keyword
    def set_element_value(
        self,
        locator: Optional[Locator] = None,
        value: Optional[str] = None,
        append: bool = False,
    ) -> WindowsElement:
        existing_content = ""
        if locator:
            element = self.get_element(locator).item
        else:
            element = auto
        existing_content = element.GetValuePattern().Value if append else ""
        element.GetValuePattern().SetValue(f"{existing_content}{value}")

    @keyword
    def send_keys(
        self,
        locator: Optional[Locator] = None,
        keys: Optional[str] = None,
        interval: float = 0.01,
        wait_time: Optional[float] = None,
        send_enter: bool = False,
        raw: bool = False,
    ) -> WindowsElement:
        if locator:
            element = self.get_element(locator).item
        else:
            element = auto
        keys_wait_time = wait_time or self.wait_time
        if send_enter:
            keys += "{Enter}"
        if hasattr(element, "SendKeys"):
            self.logger.info("Sending keys %r to element %r", keys, element)
            if raw:
                keys = get_raw_keys(keys)

            element.SendKeys(
                text=keys,
                interval=interval,
                waitTime=keys_wait_time,
            )
        else:
            raise ActionNotPossible(
                f"Element found with {locator!r} does not have 'SendKeys' attribute"
            )
