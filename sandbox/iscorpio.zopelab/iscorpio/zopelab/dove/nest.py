# nest.py

"""
a simple Zope product trying to use GenericSetup to do some initialization
work.
"""

from OFS import SimpleItem
from Globals import InitializeClass
from zope.interface import implements

from Products.CMFQuickInstallerTool.interfaces import INonInstallable

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# hide the profile from quicker installer.
class HiddenProducts(object):
    implements(INonInstallable)

    # returns a list of product names
    def getNonInstallableProducts(self):
        return ['iscorpio.zopelab.dove']

# CMFDove product class. Extends from SimpleItem to get some basic
# behavior for work with ZMI
class CMFDove(SimpleItem.SimpleItem):
    """
    A simple Zope product leverage on GenericSetup.
    """

    # specify the meta type to show up on the add drop down for a Zope
    # instance.
    meta_type = "iScorpio ZopeLab Dove"

    # __init__
    def __init__(self, id, title=''):
        """
        the initialization.
        """

        self.id = id
        self.title = title

    # the default home page for this produce.
    def index_html(self):
        """
        Just try to say something here.
        """

        return """<html><body>Welcome to %s</body></html>
        """ % self.title

InitializeClass(CMFDove)
