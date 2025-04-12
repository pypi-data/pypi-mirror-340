import re
import jwt
import json
import base64
import urllib.parse
import datetime
import vierror as vie


def trim(value, name: str = ""):
    if isinstance(value, str):
        return value.strip()
    else:
        raise vie.MError("VerifyModel.String.Trim", f"{name} 只能对字符串进行 trim 操作")
    
def regex(regex: str):
    def warpper(value, name: str = ""):
        if not re.match(regex, value):
            raise vie.MError("VerifyModel.String.Regex", f"{name}值格式不正确")
        return value
    return warpper

def email(value, name: str = ""):
    if not re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", value):
        raise vie.MError("VerifyModel.String.Email", f"邮箱{name}值格式不正确")
    return value

def phone(value, name: str = ""):
    if not re.match(r"^1[3456789]\d{9}$", value):
        raise vie.MError("VerifyModel.String.Phone", f"电话号码{name}值格式不正确")
    return value

def url(value, name: str = ""):
    if not re.match(r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$", value):
        raise vie.MError("VerifyModel.String.Url", f"网址{name}值格式不正确")
    return value

def ip(value, name: str = ""):
    if not re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", value):
        raise ValueError("VerifyModel.String.IP", f"IP地址{name}值格式不正确")
    return value

def date(format: str = "%Y-%m-%d"):
    def wapper(value, name: str = ""):
        try:
            datetime.datetime.strptime(value, format)
            return value
        except ValueError:
            raise vie.MError("VerifyModel.String.Date", f"日期{name}值格式不正确")
    return wapper

def date_time(format: str = "%Y-%m-%d %H:%M:%S"):
    def wapper(value, name: str = ""):
        try:
            datetime.datetime.strptime(value, format)
            return value
        except ValueError:
            raise vie.MError("VerifyModel.String.Datetime", f"日期时间{name}值格式不正确")
    return wapper

def time(format: str = "%H:%M:%S"):
    def wapper(value, name: str = ""):
        try:
            datetime.datetime.strptime(value, format)
            return value
        except ValueError:
            raise vie.MError("VerifyModel.String.Time", f"时间{name}值格式不正确")
    return wapper

def uuid(value, name: str = ""):
    if not re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", value):
        raise vie.MError("VerifyModel.String.UUID", f"UUID{name}值格式不正确")
    return value

def is_alpha(value, name: str = ""):
    if not value.isalpha():
        raise vie.MError("VerifyModel.String.IsAlpha", f"{name}值必须全部由字母组成")
    return value

def is_digit(value, name: str = ""):
    if not value.isdigit():
        raise vie.MError("VerifyModel.String.IsDigit", f"{name}值必须全部由数字组成")
    return value

def is_alnum(value, name: str = ""):
    if not value.isalnum():
        raise vie.MError("VerifyModel.String.IsAlnum", f"{name}值必须由字母和数字组成")
    return value

def to_upper(value, name: str = ""):
    return value.upper()

def is_upper(value, name: str = ""):
    if not value.isupper():
        raise vie.MError("VerifyModel.String.IsUpper", f"{name}值必须全部由大写字母组成")
    return value

def to_lower(value, name: str = ""):
    return value.lower()

def is_lower(value, name: str = ""):
    if not value.islower():
        raise vie.MError("VerifyModel.String.IsLower", f"{name}值必须全部由小写字母组成")
    return value

def is_json(value, name: str = ""):
    try:
        json.loads(value)
    except json.JSONDecodeError:
        raise vie.MError("VerifyModel.String.IsJson", f"{name}值不是有效的JSON字符串")
    return value

def is_base64(value, name: str = ""):
    try:
        base64.b64decode(value)
    except Exception:
        raise vie.MError("VerifyModel.String.IsBase64", f"{name}值不是有效的Base64编码")
    return value

def is_url_encoded(value, name: str = ""):
    try:
        urllib.parse.unquote(value)
    except Exception:
        raise vie.MError("VerifyModel.String.IsUrlEncoded", f"{name}值不是有效的URL编码")
    return value

def is_chinese_province(value, name: str = ""):
    provinces = [
        "北京", "天津", "上海", "重庆",
        "河北", "山西", "辽宁", "吉林", "黑龙江",
        "江苏", "浙江", "安徽", "福建", "江西", "山东",
        "河南", "湖北", "湖南", "广东", "海南",
        "四川", "贵州", "云南", "陕西", "甘肃", "青海",
        "台湾",
        "内蒙古", "广西", "西藏", "宁夏", "新疆",
        "香港", "澳门"
    ]
    if value not in provinces:
        raise vie.MError("VerifyModel.String.IsChineseProvince", f"{name}值不是中国省份名称")
    return value

def is_rgb_str(split: str = ","):
    def warpper(value, name: str = ""):
        if not re.match(r"^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$", value):
            raise vie.MError("VerifyModel.String.IsRgb", f"{name}值不是有效的RGB颜色字符串")
        return value.split(split)
    return warpper

def is_rgba_str(split: str = ","):
    def warpper(value, name: str = ""):
        if not re.match(r"^rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(0(\.\d+)?|1(\.0+)?)\s*\)$", value):
            raise vie.MError("VerifyModel.String.IsRgba", f"{name}值不是有效的RGBA颜色字符串")
        return value.split(split)
    return warpper

def is_hex_color(has_number_sign: bool = False):
    def warpper(value, name: str = ""):
        if has_number_sign:
            if not re.match(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", value):
                raise vie.MError("VerifyModel.String.IsHexColor", f"{name}值不是有效的十六进制颜色值")
        else:
            if not re.match(r"^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", value):
                raise vie.MError("VerifyModel.String.IsHexColor", f"{name}值不是有效的十六进制颜色值")
        return value
    return warpper

def decode_base64(value, name: str = ""):
    try:
        return base64.b64decode(value).decode()
    except Exception:
        raise vie.MError("VerifyModel.String.DecodeBase64", f"{name}值不是有效的Base64编码")
    
def encode_base64(value, name: str = ""):
    try:
        return base64.b64encode(value.encode()).decode()
    except Exception:
        raise vie.MError("VerifyModel.String.EncodeBase64", f"{name}值不是有效的Base64编码")

def decode_url_encoded(value, name: str = ""):
    try:
        return urllib.parse.unquote(value)
    except Exception:
        raise vie.MError("VerifyModel.String.DecodeUrlEncoded", f"{name}值不是有效的URL编码")

def encode_url_encoded(value, name: str = ""):
    try:
        return urllib.parse.quote(value)
    except Exception:
        raise vie.MError("VerifyModel.String.EncodeUrlEncoded", f"{name}值不是有效的URL编码")
    
def is_chinese(value, name: str = ""):
    if not re.match(r"^[\u4e00-\u9fa5]+$", value):
        raise vie.MError("VerifyModel.String.IsChinese", f"{name}值不是有效的中文字符串")
    return value

def is_english(value, name: str = ""):
    if not re.match(r"^[a-zA-Z]+$", value):
        raise vie.MError("VerifyModel.String.IsEnglish", f"{name}值不是有效的英文字符串")
    return value

def is_password(value, name: str = ""):
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?/~\\-]).{8,}$", value):
        raise vie.MError("VerifyModel.String.IsPassword", f"{name}值不是有效的密码")
    return value

def decode_jwt(decode_key: str):
    def warpper(value, name: str = ""):
        try:
            data = jwt.decode(value, decode_key, algorithms=["HS256"])
            return json.dumps(data)
        except Exception:
            raise vie.MError("VerifyModel.String.DecodeJwt", f"{name}值不是有效的JWT")
    return warpper