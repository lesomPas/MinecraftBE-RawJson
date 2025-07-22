

def is_single_string_value(d: dict, key_name: str) -> bool:
    """
    检查字典是否有且只有一个键，且对应的值是字符串

    argument:
        d: 待检查的字典

    return:
        bool: 如果字典只有一个键且值是字符串则返回True，否则返回False
    """
    if not isinstance(key_name, str):
        return False
    # 检查字典是否只有一个键
    if len(d) != 1:
        return False

    value = d.get(key_name, None)
    return value != None and isinstance(value, str)


def is_string_value(d: dict, keys: list[str]) -> bool:
    """
    检查字典是否有且只有keys中的键，且对应的值是字符串

    argument:
        d: 待检查的字典

    return:
        bool: 如果字典只有keys中的键且值是字符串则返回True，否则返回False
    """
    # 检查字典是否只有keys中的键
    if len(d) != len(keys):
        return False

    for key in keys:
        if not isinstance(key, str):
            return False
        value = d.get(key, None)
        if value == None or not isinstance(value, str):
            return False

    return True

def is_single_dictionary_value(d: dict, key_name: str) -> bool:
    """
    检查字典是否有且只有一个键，且对应的值是字符串

    argument:
        d: 待检查的字典

    return:
        bool: 如果字典只有一个键且值是字典则返回True，否则返回False
    """
    if not isinstance(key_name, str):
        return False
    # 检查字典是否只有一个键
    if len(d) != 1:
        return False

    value = d.get(key_name, None)
    return value != None and isinstance(value, dict)