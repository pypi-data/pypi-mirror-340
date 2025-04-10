from .res import res
import vierror as vie


def async_exception(func):
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except vie.MError as me:
            return res(False, me.dump())
        except Exception as e:
            return res(False, str(e))

    return async_wrapper


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except vie.MError as me:
            return res(False, me.dump())
        except Exception as e:
            return res(False, str(e))

    return wrapper