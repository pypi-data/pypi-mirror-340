def res(status: bool = False, err: str = "", msg: any = None):
    """
    响应
    :param status: 状态
    :param err: 错误信息
    :param msg: 消息
    :return: dict
    """
    return {
        'status': status,  # 状态
        "err": err,  # 错误信息
        "msg": msg if not msg else {},  # 消息
    }