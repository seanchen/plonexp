
# XPointArtifact.py

__doc__ = """XPointStory defines a track item for a software project in Agile approach."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import AttributeStorage
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.CMFCore.utils import getToolByName

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase

# the schema for artifact.
XPointArtifactSchema = ATFolderSchema.copy() + Schema((

        # artifact details
        TextField(
            'xppm_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Details',
                description = 'Details description for this artifact',
                rows = 18,
                ),
            ),

        # artifact status
        StringField(
              'xppm_artifact_status',
              searchable = False,
              required = True,
              default = '',
              vocabulary = 'vocabulary_artifactStatus',
              widget = SelectionWidget(
                label = "Artifact Status",
                description = "Select status for this artifact",
                format = 'select',
                ),
            ),

        # artifact category
        StringField(
              'xppm_artifact_category',
              searchable = False,
              required = True,
              default = '',
              vocabulary = 'vocabulary_categories',
              widget = SelectionWidget(
                label = 'Artifact Category',
                description = 'Select category for this artifact',
                format = 'select',
                ),
            ),

        # the priority
        StringField(
              'xppm_artifact_priority',
              searchable = False,
              required = True,
              default = '',
              vocabulary = 'vocabulary_priorities',
              widget = SelectionWidget(
                  label = 'Priority',
                  description = 'Set the priority for this artifact',
                  format = 'select',
                ),
            ),

        # story
        StringField(
            'xppm_artifact_story',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_allStoriesList',
            widget = SelectionWidget(
                  label = 'Story',
                  description = 'stories related to this artifact',
                  format = 'select',
                ),
            ),

        # tags
        LinesField(
            'xppm_artifact_tags',
            vocabulary = "vocabulary_artifactTag",
            widget = InAndOutWidget(
                label = u'Tags',
                description = "Please select the tags for this artifact",
                ),
            #schemata = 'Properties',
            ),

        # attachment
        FileField(
            'xppm_artifact_attachment',
            widget = FileWidget(
                label = "Attachment",
                description = "You may upload a file here:",
                ),
            storage = AttributeStorage(),
            ),
        )
    )

# finalize the schema.
finalizeATCTSchema(XPointArtifactSchema)

# set the description field invisible.
XPointArtifactSchema['description'].widget.visible = False

# the class.
class XPointArtifact(XPPMBase, ATFolder, HistoryAwareMixin):

    schema = XPointArtifactSchema

    meta_type = "XPointArtifact"
    portal_type = "XPointArtifact"
    archetypes_type = "XPointArtifact"

    __implements__ = (ATFolder.__implements__,
                      HistoryAwareMixin.__implements__,
                      )

    # set up the prefix for auto generated ids.
    xppm_id_prefix = 'xpa'
    # the logger.
    log = logging.getLogger("XPointProjectManagement XPointArtifact")

    # the artifact change log.
    _artifactChangeLog = []

    # preparing class security info for methods.
    security = ClassSecurityInfo()

    def vocabulary_priorities(self):
        """ returns all priority options as a vocabulary.
        """
        return DisplayList(self.getMetadataByType('priority'))

    def vocabulary_categories(self):
        """ return all category options as a vocabulary.
        """
        return DisplayList(self.getMetadataByType('category'))

    def vocabulary_artifactStatus(self):
        """ return all status options as a vocabulary.
        """
        
        return DisplayList(self.getMetadataByType('status'))

    def vocabulary_artifactTag(self):
        """ return all tags options as a vocabulary.
        """
        return DisplayList(self.getMetadataByType('tag'))

# register to the plone add-on product.
registerType(XPointArtifact, PROJECTNAME)
