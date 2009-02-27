
# XPointFuncReq.py

__doc__ = """XPointFuncReq defines a function requirment for a software project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.content.base import XPPMDocBase

# the function requirement schema
XPointFuncReqSchema = XPPMDocBase.schema.copy()

# set up label and description for generic fields.
XPointFuncReqSchema['xppm_text'].widget.label = "Function Requirement Text"
XPointFuncReqSchema['xppm_text'].widget.description = "The details explain of the function requirement."

# the classes.
class XPointFuncReq(XPPMBase, XPPMDocBase):
    """ content type for a function requirement.
    """

    schema = XPointFuncReqSchema

    meta_type = "XPointFuncReq"
    portal_type = "XPointFuncReq"
    archetype_name = "XPointFuncReq"

    __implements__ = (
        XPPMDocBase.__implements__,
        )

    xppm_id_prefix = "fr"
    log = logging.getLogger("PlonePM XPointFuncReq")

registerType(XPointFuncReq, PROJECTNAME)
