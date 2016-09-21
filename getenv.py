# coding: utf-8

import os
import __builtin__


class Env(object):
    prefix = None
    _instances = {}
    supported_types = (str, int, float, bool, )
    bool_true_values = ['1', 'true', 'True']
    bool_false_values = ['0', 'false', 'False']

    def __init__(self, key,
                 type=str,
                 default=NotImplemented):
        if self.prefix is None:
            raise ValueError('Please set prefix before using Env class')

        self.key = key.format(prefix=self.prefix)

        if type not in self.supported_types:
            raise TypeError('{} is not supported'.format(type))
        self.type = type
        type = __builtin__.type

        self.default = default
        if default is not NotImplemented and \
                default is not None and \
                not isinstance(default, self.type):
            raise TypeError(
                'default {} ({}) should be the same type of {}'.format(
                    default, type(default), self.type))

        Env._instances[self.key] = self

    def get(self):
        v = os.environ.get(self.key, None)
        if v is None:
            if self.default is NotImplemented:
                raise ValueError('value not set')
            return self.default

        # convert
        if self.type is str:
            pass
        elif self.type in [int, float]:
            try:
                v = self.type(v)
            except ValueError:
                raise ValueError('Could not convert {} to type {}'.format(v, self.type))
        elif self.type is bool:
            if v in self.bool_true_values:
                v = True
            elif v in self.bool_false_values:
                v = False
            else:
                raise ValueError(
                    'for bool type only these values are allowed: {}'.format(
                        self.bool_true_values + self.bool_false_values))
        else:
            raise TypeError('Unsupported type {}'.format(self.type))

        return v

    @classmethod
    def set_prefix(cls, prefix):
        cls.prefix = prefix
