# issue.py

__doc__ = """XPointMemo records issue for a XPoint Project."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType

from Products.XPointProjectManagement.content.xpointdoc import XPointDocument
# the configruation info for this project.
from Products.XPointProjectManagement.config import PROJECTNAME

# the XPointIssue schema.
XPointIssueSchema = XPointDocument.schema.copy()

# make description invisible.
XPointIssueSchema['description'].widget.visible = False
# make document status visible.
XPointIssueSchema['xpproject_document_status'].required = True
XPointIssueSchema['xpproject_document_status'].widget.visible = True
XPointIssueSchema['xpproject_document_status'].widget.label = \
    "Issue Status"
XPointIssueSchema['xpproject_document_status'].widget.description = \
    "Status for this issue."

# the class.
class XPointIssue(XPointDocument):
    """ XPointIssue records a issue for a XPoint Project.
    """

    schema = XPointIssueSchema

    # type and name
    meta_type = 'XPointIssue'
    portal_type = 'XPointIssue'
    archetype_name = "XP Issue"

    content_icon = 'XPIssue_icon.gif'

    _at_rename_after_creation = True
    global_allow = False
    filter_content_types = False
    allowed_content_types = []

    # allow discuss on issue.
    # comment out for Plone 3, it is just doesn't work.  Need figure
    # out the new approach for Plone 3.
    #allow_discussion = True

    security = ClassSecurityInfo()

    def vocabulary_documentStatus(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('open', 'Open'),
                            ('pending', 'Pending'),
                            ('close', 'Close'),
                            ]
                           )

# register this type to plone add-on product.
registerType(XPointIssue, PROJECTNAME)
