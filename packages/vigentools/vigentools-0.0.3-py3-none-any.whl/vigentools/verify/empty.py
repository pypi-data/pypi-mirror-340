import vierror as vie


def not_null(value, name: str = ""):
    """
    验证值是否为空
    :param value: 值
    :param name: 名称
    :return: 值
    """
    if value is None:
        raise vie.MError("VerifyModel.Empty.NotNull", f"{name}值不能为空")
    return value

def is_null(value, name: str = ""):
    """
    验证值是否为 None
    :param value: 值
    :param name: 名称
    :return: 值
    """
    if value!= None:
        raise vie.MError("VerifyModel.Empty.IsNull", f"{name}值必须为 None")
    return value

def not_empty(value, name: str = ""):
    """
    验证值是否为空字符串或空列表或空字典
    :param value: 值
    :param name: 名称
    :return: 值
    """
    if isinstance(value, str) and value.strip() == "":
        raise vie.MError("VerifyModel.Empty.NotEmpty", f"{name}值不能为空")
    elif isinstance(value, list) and len(value) == 0:
        raise vie.MError("VerifyModel.Empty.NotEmpty", f"{name}值不能为空")
    elif isinstance(value, dict) and len(value) == 0:
        raise vie.MError("VerifyModel.Empty.NotEmpty", f"{name}值不能为空")
    return value