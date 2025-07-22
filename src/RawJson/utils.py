def _is_value(d: dict, key, data_type) -> bool:
    return key in d and isinstance(d[key], data_type)


def is_single_string_value(d: dict, key) -> bool:
    """
    检查字典是否有且只有一个键，且对应的值是字符串

    argument:
        d: 待检查的字典

    return:
        bool: 如果字典只有一个键且值是字符串则返回True，否则返回False
    """
    if len(d) != 1:
        return False

    return _is_value(d, key, str)


def is_single_dictionary_value(d: dict, key) -> bool:
    """
    检查字典是否有且只有一个键，且对应的值是字符串

    argument:
        d: 待检查的字典

    return:
        bool: 如果字典只有一个键且值是字典则返回True，否则返回False
    """
    if len(d) != 1:
        return False

    return _is_value(d, key, dict)


def is_string_value(d: dict, keys: list) -> bool:
    """
    检查字典是否有且只有keys中的键，且对应的值是字符串

    argument:
        d: 待检查的字典

    return:
        bool: 如果字典只有keys中的键且值是字符串则返回True，否则返回False
    """
    if len(d) != len(keys):
        return False

    return all(_is_value(d, key, str) for key in keys)