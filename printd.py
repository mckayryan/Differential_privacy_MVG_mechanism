import pprint

DEBUG_LEVEL = 4


def printd(to_print, level=1, **kwargs):
    if DEBUG_LEVEL >= level:
        if isinstance(to_print, str):
            pprint.pprint(to_print.format(**kwargs))
        else:
            pprint.pprint(to_print)
