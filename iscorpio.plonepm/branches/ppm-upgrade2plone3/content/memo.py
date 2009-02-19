# memo.py

__doc__ = """XPointMemo defines the memo for a XPoint Project."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import registerType

from Products.XPointProjectManagement.content.xpointdoc import XPointDocument
# the configruation info for this project.
from Products.XPointProjectManagement.config import PROJECTNAME

# define the schem for XPointMemo.
XPointMemoSchema = XPointDocument.schema.copy()

# we don't need descrpiton field for a memo.
XPointMemoSchema['description'].widget.visible = False

# XPointMemo class.
class XPointMemo(XPointDocument):
    """ XPointMemo defines the note for a XPoint Project.
    """

    schema = XPointMemoSchema

    # type, name.
    meta_type = 'XPointMemo'
    portal_type = 'XPointMemo'
    archetype_name = 'XP Memo'

    content_icon = 'XPMemo_icon.gif'

    _at_rename_after_creation = True
    global_allow = False
    filter_content_types = False
    allowed_content_types = []

    # allow discuss on memo.
    # comment out for Plone 3, it is just doesn't work.  Need figure
    # out the new approach for Plone 3.
    #allow_discussion = True

    security = ClassSecurityInfo()


def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata']:
            a['visible'] = 0
    return fti

# register this type to plone add-on product.
registerType(XPointMemo, PROJECTNAME)
