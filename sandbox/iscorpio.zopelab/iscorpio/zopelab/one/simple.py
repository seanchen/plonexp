# simple.py

"""
A very simple Zope product.
"""

from OFS import SimpleItem

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the simple product class.
# Extends SimpleItem to make our SimpleProduct to have the basic needs
# for work with Zope Management Interface.
class SimpleProduct(SimpleItem.SimpleItem):
    """
    A very simple Zope product.
    """

    # The metatype will be used by Zope server to add our
    # SimpleProduct to any folder in the Zope Server.  It should be
    # unique and you will see it in the dropdown selection box.
    meta_type = "iScorpio ZopeLab Simple Product"

    # any object in Zope Server needs a id, which should be set during
    # initialization. 
    def __init__(self, id):
        """
        Initialize a new instance of SimpleProduct.
        """

        self.id = id

    # our first method to print out hello world.
    def index_html(self):
        """
        Print out the string hello world.
        """

        return """<html><body>Hello, Welcome to my first Simple Zope
        Product!</body></html>
        """

# facility method to create a new instance of SimpleProduct.
def manage_addSimpleProduct(self, REQUEST):
    """
    This method will be called by an ObjectManager, normally a Folder,
    when we selected the 'iScorpio ZopeLab Simple Product' from the
    Add dropdown selection box.
    """

    self._setObject('simple_id', SimpleProduct('simple_id'))
    REQUEST['RESPONSE'].redirect('%s/index_html' % self.simple_id.absolute_url(),
                                 lock=1)
