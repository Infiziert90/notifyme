from . import dispatcher


def run_me():
    def decorator(func):
        dispatcher.register(func)
        return func

    return decorator