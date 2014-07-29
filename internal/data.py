__author__ = 'Gareth Coles'

"""
Data - a database wrapper for getting various bits of data.

I created this to keep the logic out of the routes, which is important.
"""

from internal.singleton import Singleton


class Data(object):
    __metaclass__ = Singleton

    def __init__(self, manager):
        self.manager = manager
