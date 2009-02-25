# PRMResources.py

__doc__ = """PRMResources is a Plone foler resources management"""
__author__ = "iscorpio@users.sourceforge.net"
__docformat__ = 'plaintext'

# PRMResources is a ATFolder in Plone.

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import registerType
# from ATContenttypes
from Products.ATContentTypes.interfaces import IATFolder
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from iscorpio.plonerm.config import PROJECTNAME

# define the schema...
PRMResourcesSchema = ATFolderSchema.copy() + Schema((

        # the available manufacturers.
        LinesField(
            'prmManufacturers',
            searchable = False,
            required = True,
            widget = LinesWidget(
                label = 'Avilable Manufacturers',
                description = 'Please specify available manufactures. One line for each',
                ),
            ),

        # The unique sequence will serve all resources managed under here.
        IntegerField(
            'prmUniqueSequence',
            default = 0,
            # hide for view mode.
            widget = IntegerWidget(
                label = 'Unique Sequence',
                description = 'This sequence will generate unique ids for this address book',
                ),
            ),

        ),
    )

finalizeATCTSchema(PRMResourcesSchema)

# define the class.
class PRMResources(ATFolder):
    """
    Resources folder for managing resources.
    """

    schema = PRMResourcesSchema

    # type and name for Plone.
    meta_type = 'PRMResources'
    portal_type = 'PRMResources'
    archetypes_name = 'PRMResources'

    _at_rename_after_creation = True

    __implements__ = (
        ATFolder.__implements__,
        IATFolder,
        )

    security = ClassSecurityInfo()

    security.declareProtected('Modify portal content', 'getNextUniqueId')
    def getNextUniqueId(self):
        """ Return the next value from the unique sequence, and
            update the sequence itself.
        """

        newId = self.prmUniqueSequence + 1
        self.setPrmUniqueSequence(newId)
        return newId

# register...
registerType(PRMResources, PROJECTNAME)
