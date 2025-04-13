def with_args(*args):
    data = []
    for arg in args:
        data.append(arg * 100)
    return data

def with_args_with_i(*args, **kwargs):
    data = []
    if not kwargs.get("i"):
        raise AttributeError("missing i arg")
    for arg in args:
        data.append(arg * 100)
    return data