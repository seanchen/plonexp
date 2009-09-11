# factory.py

"""
here we will defined the form the action method to create an
instance of CMFDove.
"""

from Globals import DTMLFile
from nest import CMFDove

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the intialize form.
manage_addDoveForm = DTMLFile('www/addCMFDove', globals())

# create the CMFDove inatance.
def manage_addDove(self, id, title='', REQUEST=None):
    """
    
    """

    self._setObject(id, CMFDove(id, title))
    if REQUEST:
        REQUEST['RESPONSE'].redirect('%s/%s/index_html' % (self.absolute_url(), id),
                                     lock=1)
