#!/usr/bin/env python3
# coding=utf-8

"""
@author: guoyanfeng
@software: PyCharm
@time: 18-12-25 下午2:08
"""
from typing import Any, Optional

__all__ = ("HttpError", "FuncArgsError", "Error", "MongoError", "MongoDuplicateKeyError",
           "MongoInvalidNameError", "ConfigError")


class Error(Exception):
    """
    异常基类
    """

    def __init__(self, message: Optional[str] = None):
        self.message: Optional[str] = message

    def __str__(self):
        return "Error: message='{}'".format(self.message)

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.message)


class HttpError(Error):
    """
    主要处理http 错误,从接口返回
    """

    def __init__(self, status_code: int, *, message: Optional[str] = None, error: Optional[Any] = None):
        self.status_code: int = status_code
        self.message: Optional[str] = message
        self.error: Optional[Any] = error

    def __str__(self):
        return "{}, '{}':'{}'".format(self.status_code, self.message, self.message or self.error)

    def __repr__(self):
        return "<{} '{}: {}'>".format(self.__class__.__name__, self.status_code, self.error or self.message)


class MongoError(Error):
    """
    主要处理mongo错误
    """

    pass


class MongoDuplicateKeyError(MongoError):
    """
    处理键重复引发的error
    """

    pass


class MongoInvalidNameError(MongoError):
    """
    处理名称错误引发的error
    """

    pass


class FuncArgsError(Error):
    """
    处理函数参数不匹配引发的error
    """

    pass


class ConfigError(Error):
    """
    主要处理config error
    """

    pass
