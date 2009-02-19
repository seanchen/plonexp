
# XPointUseCase.py

__doc__ = """XPointUseCases defines a use case for a software project.
A use case could explain a funcationality from function specification.
"""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

# the configruation info for this project.
from Products.XPointProjectManagement.config import PROJECTNAME
from Products.XPointProjectManagement.content.base import XPPMBase
from Products.XPointProjectManagement.content.base import XPPMDocBase

# the use case schema.
XPointUseCaseSchema = XPPMDocBase.schema.copy()

# set up the label and description for generic field.
XPointUseCaseSchema['xppm_text'].widget.label = "Use Case Text"
XPointUseCaseSchema['xppm_text'].widget.description = "Details explain for this use case."

# the use case class.
class XPointUseCase(XPPMBase, XPPMDocBase):
    """ content type class for a use case.
    """

    schema = XPointUseCaseSchema

    meta_type = "XPointUseCase"
    portal_type = "XPointUseCase"
    archetype_name = "XPointUseCase"

    __implements__ = (
        XPPMDocBase.__implements__,
        )

    xppm_id_prefix = "uc"
    log = logging.getLogger("XPointProjectManagement XPointUseCase")
    security = ClassSecurityInfo()

registerType(XPointUseCase, PROJECTNAME)
