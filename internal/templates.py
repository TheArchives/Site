__author__ = 'Gareth Coles'

"""
Templates - For getting various templates and required data for them

This class will do the heavy lifting of the template logic, to keep it from the
routes.
"""

from internal.singleton import Singleton


class Templates(object):
    __metaclass__ = Singleton

    def __init__(self, manager):
        self.manager = manager
