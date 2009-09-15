# factory.py

"""
here we will defined the form the action method to create an
instance of CMFDove.
"""

from Acquisition import aq_inner, aq_parent
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

    dove = self._getOb(id)
    parent = aq_parent(aq_inner(self))
    parent.Plone.portal_setup.runAllImportStepsFromProfile('profile-iscorpio.zopelab.dove:dove')

    if REQUEST:
        REQUEST['RESPONSE'].redirect('%s/index_html' % dove.absolute_url(),
                                     lock=1)
