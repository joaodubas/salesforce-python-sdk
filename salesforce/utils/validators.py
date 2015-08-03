# encoding: utf-8


def validate_boolean_input(value, name):
    if value not in (True, False):
        raise TypeError('{} should be True or False'.format(name))
