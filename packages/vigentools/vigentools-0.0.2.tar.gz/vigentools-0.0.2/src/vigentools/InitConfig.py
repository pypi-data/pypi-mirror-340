import pathlib
import viconfig as vic


def init_config(list_fields: list[vic.Field]):
    config = vic.Config()
    config.add_fields(list_fields)

    config_obj = pathlib.Path('config.json')
    if config_obj.exists():
        config.load_from_json('config.json')
    else:
        config.save_to_json("config.json")

    return config