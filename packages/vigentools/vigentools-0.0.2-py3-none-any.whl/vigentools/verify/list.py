import vierror as vie


def in_list(lst: list):
    """
    验证值是否在列表中。

    参数:
        lst (list): 要验证的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        list: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def wapper(value, name: str = ""):
        if value not in lst:
            raise vie.MError("VerifyModel.List.InList", f"{name}值不在列表中")
        return value
    return wapper

def not_in_list(lst: list):
    """
    验证值是否不在列表中。

    参数:
        lst (list): 要验证的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        list: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def wapper(value, name: str = ""):
        if value in lst:
            raise vie.MError("VerifyModel.List.NotInList", f"{name}值在列表中")
        return value
    return wapper

def list_is_unique(value: list, name: str = ""):
    """
    验证列表中的所有值是否唯一。

    参数:
        value (list): 要验证的列表。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        list: 验证通过的列表。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if len(value)!= len(set(value)):
        raise vie.MError("VerifyModel.List.ListIsUnique", f"{name}值必须为唯一")
    return value

def list_is_not_unique(value: list, name: str = ""):
    """
    验证列表中的所有值是否不唯一。

    参数:
        value (list): 要验证的列表。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        list: 验证通过的列表。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if len(value) == len(set(value)):
        raise vie.MError("VerifyModel.List.ListIsNotUnique", f"{name}值必须为不唯一")
    return value

def is_rgb(value: list, name: str = ""):
    """
    验证值是否是有效的RGB颜色值。

    参数:
        value (list): 要验证的RGB颜色值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        list: 验证通过的RGB颜色值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if len(value) != 3 or not all(isinstance(x, int) and 0 <= x <= 255 for x in value):
        raise vie.MError("VerifyModel.List.IsRgb", f"{name}值不是有效的RGB颜色值")
    return value

def is_rgba(value: list, name: str = ""):
    """
    验证值是否是有效的RGBA颜色值。

    参数:
        value (list): 要验证的RGBA颜色值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        list: 验证通过的RGBA颜色值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if len(value) != 4 or not all(isinstance(x, int) and 0 <= x <= 255 for x in value[:3]) or not (isinstance(value[3], float) and 0 <= value[3] <= 1):
        raise vie.MError("VerifyModel.General.IsRgba", f"{name}值不是有效的RGBA颜色值")
    return value