import vierror as vie


def max_len(max_len: int):
    def warpper(value, name: str = ""):
        if len(value) > max_len:
            raise vie.MError("VerifyModel.General.MaxLen", f"{name}值长度不能超过 {max_len}")
        return value
    return warpper

def min_len(min_len: int):
    def warpper(value, name: str = ""):
        if len(value) < min_len:
            raise vie.MError("VerifyModel.General.MinLen", f"{name}值长度不能小于 {min_len}")
        return value
    return warpper

def equal(value):
    def wapper(v, name: str = ""):
        if v != value:
            raise vie.MError("VerifyModel.General.Equal", f"{name}值不等于 {value}")
        return v
    return wapper

def not_equal(value):
    def wapper(v, name: str = ""):
        if v== value:
            raise vie.MError("VerifyModel.General.NotEqual", f"{name}值等于 {value}")
        return v
    return wapper