import datetime
import vierror as vie

def min(min: int):
    """
    验证值是否大于或等于指定的最小值。

    参数:
        min (int): 最小值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def warpper(value, name: str = ""):
        if value < min:
            raise vie.MError("VerifyModel.Number.Min", f"{name}值不能小于 {min}")
        return value
    return warpper

def max(max: int):
    """
    验证值是否小于或等于指定的最大值。

    参数:
        max (int): 最大值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def warpper(value, name: str = ""):
        if value > max:
            raise vie.MError("VerifyModel.Number.Max", f"{name}值不能大于 {max}")
        return value
    return warpper

def greater_than(value):
    """
    验证值是否大于指定的值。

    参数:
        value (int): 要比较的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def wapper(v, name: str = ""):
        if v<= value:
            raise vie.MError("VerifyModel.Number.GreaterThen", f"{name}值小于等于 {value}")
        return v
    return wapper

def less_than(value):
    """
    验证值是否小于指定的值。

    参数:
        value (int): 要比较的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def wapper(v, name: str = ""):
        if v>= value:
            raise vie.MError("VerifyModel.Number.LessThen", f"{name}值大于等于 {value}")
        return v
    return wapper

def greater_than_or_equal(value):
    """
    验证值是否大于或等于指定的值。

    参数:
        value (int): 要比较的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def wapper(v, name: str = ""):
        if v< value:
            raise vie.MError("VerifyModel.Number.GreaterThenOrEqual", f"{name}值小于 {value}")
        return v
    return wapper

def less_than_or_equal(value):
    """
    验证值是否小于或等于指定的值。

    参数:
        value (int): 要比较的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    def wapper(v, name: str = ""):
        if v> value:
            raise vie.MError("VerifyModel.Number.LessThenOrEqual", f"{name}值大于 {value}")
        return v
    return wapper

def is_even(value, name: str = ""):
    """
    验证值是否为偶数。

    参数:
        value (int): 要验证的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if value % 2 != 0:
        raise vie.MError("VerifyModel.Number.IsEven", f"{name}值必须是偶数")
    return value

def is_odd(value, name: str = ""):
    """
    验证值是否为奇数。

    参数:
        value (int): 要验证的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if value % 2 == 0:
        raise vie.MError("VerifyModel.Number.IsOdd", f"{name}值必须是奇数")
    return value

def is_prime(value, name: str = ""):
    """
    验证值是否为素数。

    参数:
        value (int): 要验证的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    if value <= 1:
        raise vie.MError("VerifyModel.Number.IsPrime", f"{name}值必须是大于1的整数")
    for i in range(2, int(value ** 0.5) + 1):
        if value % i == 0:
            raise vie.MError("VerifyModel.Number.IsPrime", f"{name}值必须是素数")
    return value

def is_timestamp(value, name: str = ""):
    """
    验证值是否为时间戳。

    参数:
        value (int): 要验证的值。
        name (str, 可选): 验证失败时的错误信息中的名称。默认为空字符串。

    返回:
        int: 验证通过的值。

    抛出:
        vie.MError: 如果验证失败，抛出一个错误。
    """
    try:
        value = int(value)
        if value < 0:
            raise vie.MError("VerifyModel.Number.IsTimestamp", f"{name}值必须是大于0的整数")
        datetime.datetime.fromtimestamp(value)
    except (ValueError, OverflowError, OSError):
        raise vie.MError("VerifyModel.Number.IsTimestamp", f"{name}值不是有效的时间戳")
    return value