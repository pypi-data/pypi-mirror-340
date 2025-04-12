import os
import re
import vierror as vie


def path_is_file(value: str, name: str = ""):
    if not os.path.isfile(value):
        raise vie.MError("VerifyModel.Path.IsFile", f"{name}值必须为文件")
    return os.path.normpath(value)

def path_is_dir(value: str, name: str = ""):
    if not os.path.isdir(value):
        raise vie.MError("VerifyModel.Path.IsDir", f"{name}值必须为目录")
    return os.path.normpath(value)

def path_is_exist(value: str, name: str = ""):
    if not os.path.exists(value):
        raise vie.MError("VerifyModel.Path.Exist", f"{name}值必须存在")
    return os.path.normpath(value)

def path_is_not_exist(value: str, name: str = ""):
    if os.path.exists(value):
        raise vie.MError("VerifyModel.Path.NotExist", f"{name}值必须不存在")
    return os.path.normpath(value)

def create_path(value: str, name: str = ""):
    if not os.path.exists(value):
        os.makedirs(value)
    else:
        raise vie.MError("VerifyModel.Path.CreatePath", f"{name}值必须不存在")
    return os.path.normpath(value)

def delete_path(value: str, name: str = ""):
    if os.path.exists(value):
        os.remove(value)
    else:
        raise vie.MError("VerifyModel.Path.DeletePath", f"{name}值必须存在")
    return os.path.normpath(value)

def is_special_file(format: str = ""):
    def wapper(value, name: str = ""):
        if not re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" + format + "$", value):
            raise vie.MError("VerifyModel.Path.SpecialFile", f"特殊文件{name}值格式不正确")
        return value
    return wapper