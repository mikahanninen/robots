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
