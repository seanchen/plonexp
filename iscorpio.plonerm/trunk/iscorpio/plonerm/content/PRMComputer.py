# PRMComputer.py

__doc__ = """PRMComputer defines a computer's information"""
__author__ = "iscorpio@users.sourceforge.net"
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.configuration import zconf

from Products.statusmessages.interfaces import IStatusMessage

from iscorpio.plonerm.config import PROJECTNAME
from iscorpio.plonerm.content.base import PRMBaseContent

PRMComputerSchema = ATCTContent.schema.copy() + Schema((

        StringField(
            'prmManufacturer',
            default = 'Unknow',
            vocabulary = 'vocabularyManufacturers',
            widget = SelectionWidget(
                label = "Computer Manufacturer",
                description = 'Please pick the manufacturer for this computer',
                format = 'select',
                ),
            ),
        ),
    )

finalizeATCTSchema(PRMComputerSchema)

class PRMComputer(PRMBaseContent, ATCTContent):
    """ This will be a document for hosting computer's information.
    """

    schema = PRMComputerSchema

    meta_type = 'PRMComputer'
    portal_type = 'PRMComputer'
    archetype_name = 'PRMComputer'

    _at_rename_after_creation = True

    __implements__ = (
        ATCTContent.__implements__,
        IATDocument,
        )

    # set the prefix for the id.
    prm_id_prefix = "prmc"

    security = ClassSecurityInfo()

    security.declarePrivate('vocabularyManufacturers')
    def vocabularyManufacturers(self):
        """ return all the manufacturers as a DisplayList.
        """
        manus = self.getPrmManufacturers()
        return DisplayList(zip(manus, manus))

registerType(PRMComputer, PROJECTNAME)
