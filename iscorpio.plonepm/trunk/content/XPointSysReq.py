
# XPointSysReq.py

__doc__ = """XPointSysReq defines a system requirment for a software project."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from Products.XPointProjectManagement.config import PROJECTNAME
from Products.XPointProjectManagement.content.base import XPPMBase
from Products.XPointProjectManagement.content.base import XPPMDocBase

# the function requirement schema
XPointSysReqSchema = XPPMDocBase.schema.copy()

# set up label and description for generic fields.
XPointSysReqSchema['xppm_text'].widget.label = "System Requirement Text"
XPointSysReqSchema['xppm_text'].widget.description = "The details explain of the system requirement."

# the classes.
class XPointSysReq(XPPMBase, XPPMDocBase):
    """ content type for a system requirement.
    """

    schema = XPointSysReqSchema

    meta_type = "XPointSysReq"
    portal_type = "XPointSysReq"
    archetype_name = "XPointSysReq"

    __implements__ = (
        XPPMDocBase.__implements__,
        )

    xppm_id_prefix = "sr"
    log = logging.getLogger("XPointProjectManagement XPointSysReq")

registerType(XPointSysReq, PROJECTNAME)
