import vierror as vie


def is_true(value, name: str = ""):
    if value != True:
        raise vie.MError("VerifyModel.Bool", f"{name}值必须为 True")
    return value

def is_false(value, name: str = ""):
    if value != False:
        raise vie.MError("VerifyModel.Bool", f"{name}值必须为 False")
    return value