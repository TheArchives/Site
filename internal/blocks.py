__author__ = 'Gareth Coles'

"""
Blocks - modular sections of the site

This class is for collecting and managing blocks of various sections.
"""

from internal.singleton import Singleton


class Blocks(object):
    __metaclass__ = Singleton

    def __init__(self, manager):
        self.manager = manager
