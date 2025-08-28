# -*- coding: utf-8 -*-
import functools
from traceback import print_exc


def error_handler(func):
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_exc()
            raise e

    return sync_wrapper
