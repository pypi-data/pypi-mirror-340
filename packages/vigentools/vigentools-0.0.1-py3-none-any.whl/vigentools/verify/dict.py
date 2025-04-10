import vierror as vie


def dict_has_key(key: str | list[str]):
    """
    验证字典是否包含指定的键或键列表中的所有键。

    参数:
        key (str | list[str]): 要验证的键或键列表。

    返回:
        验证通过的字典。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if isinstance(key, str):
        def warpper(value, name: str = ""):
            if key not in value:
                raise vie.MError("VerifyModel.Object", f"{name}值中必须包含键 {key}")
            return value
        return warpper 
    elif isinstance(key, list):
        def warpper(value, name: str = ""):
            for k in key:
                if k not in value:
                    raise vie.MError("VerifyModel.Object", f"{name}值中必须包含键 {k}")
            return value
        return warpper
    else:
        raise vie.MError("VerifyModel.Object.TypeError", "key must be str or list[str]")

def dict_has_value(value: dict, name: str = ""):
    """
    验证字典是否包含值。

    参数:
        value (dict): 要验证的字典。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        dict: 验证通过的字典。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if len(value.values()) == 0:
        raise vie.MError("VerifyModel.Object", f"{name}值中必须包含值")
    return value

def dict_all_values_satisfy(func, value: dict, name: str = ""):
    """
    验证字典中的所有值是否满足指定的条件。

    参数:
        func (callable): 用于验证值的函数。
        value (dict): 要验证的字典。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        dict: 验证通过的字典。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    for v in value.values():
        func(v, name)
    return value