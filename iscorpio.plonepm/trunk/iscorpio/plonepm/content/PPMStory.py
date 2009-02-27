
# PPMStory.py

__doc__ = """PPMStory defines a story for a software project in Agile approach."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase

# the schema for story.
PPMStorySchema = ATFolderSchema.copy() + Schema((

        # scope details
        TextField(
            'xppm_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Details',
                description = 'Details description for this story',
                rows = 18,
                ),
            ),

        # Assumptions or pre-request.
        TextField(
            'xppm_story_assumptions',
            searchable = True,
            required = False,
            default_content_type = 'text/plain',
            allowable_content_types = ('text/plain',),
            widget=TextAreaWidget(
                label = 'Assumptions',
                description = 'A short summary of the assumputions for your story',
                ),
            ),

        # depended stories list.
        LinesField(
            'xppm_story_dependencies',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_allStoriesList',
            widget = InAndOutWidget(
                label = 'Dependencies Stories',
                description = 'Please select dependencies stories',
                ),
            ),

        # system requirements list.
        LinesField(
            'xppm_story_sysreqs',
            searchable = False,
            required = True,
            vocabulary = 'vocabulary_allSysreqsList',
            widget = InAndOutWidget(
                label = 'System Requirements',
                description = 'Please select system requirements for your story',
                ),
            ),
        )
    )

# finalize the schema.
finalizeATCTSchema(PPMStorySchema)

# set the description field invisible.
PPMStorySchema['description'].widget.visible = False

# the class.
class PPMStory(XPPMBase, ATFolder, HistoryAwareMixin):

    schema = PPMStorySchema

    meta_type = "PPMStory"
    portal_type = "PPMStory"
    archetypes_type = "PPMStory"

    __implements__ = (ATFolder.__implements__,
                      HistoryAwareMixin.__implements__,
                      )

    # set up the prefix for auto generated ids.
    xppm_id_prefix = 'xps'
    # the logger.
    log = logging.getLogger("PlonePM PPMStory")
    # preparing class security info for methods.
    security = ClassSecurityInfo()

    security.declarePublic('vocabulary_allSysreqsList')
    def vocabulary_allSysreqsList(self):
        """ Returns a display list for all system requirement, the format is
        like [id, id + title]
        """

        ret = []
        for req in self.getAllSysReqs():
            ret.append((req.id, req.id + ' ' + req.Title))

        self.log.debug('we got %s system requirement', len(ret))
        return DisplayList(ret)

# register to the plone add-on product.
registerType(PPMStory, PROJECTNAME)
