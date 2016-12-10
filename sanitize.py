def sanitizeList(lst, sanitizer):
    retVal = []
    for item in lst:
        retVal.append(sanitize(item, sanitizer))
    return retVal

def sanitizeDict(dct, sanitizer):
    retVal = {}
    for (key, value) in dct.items():
        retVal[sanitize(key, sanitizer)] = sanitize(value, sanitizer)
    return retVal

def sanitize(value, sanitizer):
    if type(value) not in [list, dict]:
        return sanitizer(value)
    if type(value) == list:
        return sanitizeList(value, sanitizer)
    else:
        return sanitizeDict(value, sanitizer)