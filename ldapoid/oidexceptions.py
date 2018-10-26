# -*- coding: utf-8 -*-
import logging


class OidException(Exception):
    pass


class TnsAlreadyExists(OidException):
    def __init__(self, msg, *args):
        # logging.error(msg, *args)
        super(TnsAlreadyExists, self).__init__(msg, *args)


class TnsDeleteError(OidException):
    def __init__(self, msg, *args):
        # logging.error(msg, *args)
        super(TnsDeleteError, self).__init__(msg, *args)