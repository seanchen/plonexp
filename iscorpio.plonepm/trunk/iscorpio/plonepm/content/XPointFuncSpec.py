
# XPointFuncSpec.py

__doc__ = """XPointFuncSpec defines a function specification document for a software project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase

# define a XPointProject as a folder in plone site.
XPointFuncSpecSchema = ATFolderSchema.copy() + Schema((

        # the function specificaion docuemnt.
        FileField(
            'xppm_fsd',
            required = True,
            searchable = True,
            storage = AnnotationStorage(migrate = True),
            widget = FileWidget(
                label = 'Document',
                description = 'The function specification docuement',
                ),
            ),
        )
    )

finalizeATCTSchema(XPointFuncSpecSchema);

# the corresponding class file.
class XPointFuncSpec(XPPMBase, ATFolder, HistoryAwareMixin):
    """ defines a content type for function specification docuemtn.
    """

    schema = XPointFuncSpecSchema

    # type, name
    meta_type = 'XPointFuncSpec'
    portal_type = 'XPointFuncSpec'
    archetypes_type = 'XPointFuncSpec'

    __implements__ = (
        ATFolder.__implements__,
        HistoryAwareMixin.__implements__,
        )

    # set the unique id prefix.
    xppm_id_prefix = "fsd"

    log = logging.getLogger('XPointProjectManagement FSD')

    security = ClassSecurityInfo()

    # all user cases;
    security.declarePublic('getUseCases')
    def getUseCases(self):
        """ return all use cases in the FSD.
        """
        return

registerType(XPointFuncSpec, PROJECTNAME)
