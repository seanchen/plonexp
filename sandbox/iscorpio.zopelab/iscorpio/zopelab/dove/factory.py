# factory.py

"""
here we will defined the form the action method to create an
instance of CMFDove.
"""

from Acquisition import aq_inner, aq_parent
from Globals import DTMLFile
from Products.GenericSetup.tool import SetupTool
from nest import CMFDove

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

_SETUP_TOOL_ID = 'dove_setup'
_DOVE_PROFILE_ID = 'iscorpio.zopelab.dove:dove'

# the intialize form.
manage_addDoveForm = DTMLFile('www/addCMFDove', globals())

# create the CMFDove inatance.
def manage_addDove(self, id, title='', REQUEST=None):
    """
    
    """

    self._setObject(id, CMFDove(id, title))

    dove = self._getOb(id)
    # add generic set up tool for dove.
    dove._setObject(_SETUP_TOOL_ID, SetupTool(_SETUP_TOOL_ID))
    setup_tool = getattr(dove, _SETUP_TOOL_ID)
    #parent = aq_parent(aq_inner(self))
    #parent.Plone.portal_setup.runAllImportStepsFromProfile('profile-iscorpio.zopelab.dove:dove')
    setup_tool.runAllImportStepsFromProfile('profile-%s' % _DOVE_PROFILE_ID)

    if REQUEST:
        REQUEST['RESPONSE'].redirect('%s/index_html' % dove.absolute_url(),
                                     lock=1)
