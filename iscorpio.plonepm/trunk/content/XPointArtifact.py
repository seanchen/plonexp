
# XPointArtifact.py

__doc__ = """XPointStory defines a track item for a software project in Agile approach."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

# the configruation info for this project.
from Products.XPointProjectManagement.config import PROJECTNAME
from Products.XPointProjectManagement.content.base import XPPMBase

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

        # attachment
        
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
    # preparing class security info for methods.
    security = ClassSecurityInfo()

    def vocabulary_priorities(self):
        """ returns all priority options as a vocabulary.
        """
        return DisplayList([('1', '1 - Highest'),
                            ('2', '2 - High'),
                            ('3', '3 - Medium'),
                            ('4', '4 - Low'),
                            ('5', '5 - Lowest'),
                            ]
                           )

    def vocabulary_categories(self):
        """ return all category options as a vocabulary.
        """
        return DisplayList([('1', 'Issue'),
                            ('2', 'Defect'),
                            ('3', 'Proposal'),
                            ])

    def vocabulary_artifactStatus(self):
        """ return all status options as a vocabulary.
        """
        return DisplayList([('1', 'New'),
                            ('2', 'Open'),
                            ('3', 'Pending Fix'),
                            ('4', 'Pending Review'),
                            ('5', 'Pending New Build'),
                            ('6', 'Pending QA'),
                            ('7', 'Close'),
                            ])

# register to the plone add-on product.
registerType(XPointArtifact, PROJECTNAME)
