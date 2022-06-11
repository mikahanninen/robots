from RPA.Desktop.Windows import Windows


def get_raw_keys(keys):
    raw_text = ""
    for k in keys:
        if k == "{":
            raw_text += "{{}"
        elif k == "}":
            raw_text += "{}}"
        else:
            raw_text += k
    raw_text = raw_text.replace(" ", "{VK_SPACE}")
    return raw_text


class ExtendedDesktopWindows(Windows):
    def __init__(self, *args, **kwargs):
        Windows.__init__(self, *args, **kwargs)

    def type_into(
        self, locator: str, keys: str, empty_field: bool = False, raw: bool = False
    ) -> None:
        elements, _ = self.find_element(locator)
        if elements and len(elements) == 1:
            ctrl = elements[0]["control"]
            empty_method = "^a{BACKSPACE}" if empty_field else ""
            if raw:
                keys = get_raw_keys(keys)
            ctrl.type_keys(f"{empty_method}{keys}")
        else:
            raise ValueError(f"Could not find unique element for '{locator}'")
