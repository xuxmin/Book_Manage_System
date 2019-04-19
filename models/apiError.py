#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import inspect
import functools

__author__ = 'Michael Liao'

'''
JSON API definition.

客户端调用API时，必须通过错误代码来区分API调用是否成功。
错误代码是用来告诉调用者出错的原因。很多API用一个整数表示错误码，
这种方式很难维护错误码，客户端拿到错误码还需要查表得知错误信息。
更好的方式是用字符串表示错误代码，不需要看文档也能猜到错误原因。
'''

class APIError(Exception):
    '''
    the base APIError which contains error(required),  message(optional).
    '''

    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.message = message


class APIValueError(APIError):
    '''
    Indicate the input value has error or invalid. 
    '''

    def __init__(self, message=''):
        super(APIValueError, self).__init__('value:invalid', message)


class APIResourceNotFoundError(APIError):
    '''
    Indicate the resource was not found. The data specifies the resource name.
    '''

    def __init__(self, message=''):
        super(APIResourceNotFoundError, self).__init__(
            'value:notfound', message)


class APIPermissionError(APIError):
    '''
    Indicate the api has no permission.
    '''

    def __init__(self, message=''):
        super(APIPermissionError, self).__init__(
            'permission:forbidden', message)
