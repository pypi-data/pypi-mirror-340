import pathlib
import viconfig as vic


def init_config():
    config = vic.Config()
    config.add_fields([
        vic.Field('app', 'name', vic.f_string, 'LAYERS-API'),
        vic.Field('app', 'version', vic.f_string, '1.0.0'),
        vic.Field('app', 'description', vic.f_string, '图层信息表信息管理系统（服务器）'),
        vic.Field('app', 'port', vic.f_int, 8005),
        vic.Field('database', 'user', vic.f_string, "zhoubin"),
        vic.Field('database', 'password', vic.f_string, "zyb642855"),
        vic.Field('database', 'host', vic.f_string, "5.tcp.cpolar.cn"),
        vic.Field('database', 'port', vic.f_int, 13899),
        vic.Field('database', 'name', vic.f_string, "hbsk")
    ])

    config_obj = pathlib.Path('config.json')
    if config_obj.exists():
        config.load_from_json('config.json')
    else:
        config.save_to_json("config.json")

    return config