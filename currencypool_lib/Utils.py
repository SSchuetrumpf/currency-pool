from .Constants import ScriptName


def parse_parameters(parameters, message, **kwargs):
    for key in parameters.keys():
        message = message.replace(key, str(parameters[key](**kwargs)))
    return message


def tail(l):
    return l[1::]


def default_args(args=None):
    return [] if args is None else args


def log(parent, message):
    parent.Log(ScriptName, str(message))
