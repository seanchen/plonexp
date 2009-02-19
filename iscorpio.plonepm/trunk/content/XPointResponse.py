
# XPointResponse.py

__doc__ = """XPointResponse defines a """
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging
from time import strftime

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import AttributeStorage
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

# the configruation info for this project.
from Products.XPointProjectManagement.config import PROJECTNAME
from Products.XPointProjectManagement.content.base import XPPMBase

# define a XPointProject as a folder in plone site.
XPointResponseSchema = ATCTContent.schema.copy() + Schema((

        # artifact details
        TextField(
            'xppm_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Details',
                description = 'Details description for your response',
                rows = 18,
                ),
            ),

        # artifact status
        StringField(
              'xppm_response_status',
              mutator = 'setXppm_response_status',
              searchable = False,
              required = True,
              vocabulary = 'vocabulary_artifactStatus',
              widget = SelectionWidget(
                label = "Artifact Status",
                description = "Select new status for this artifact",
                format = 'select',
                ),
              default_method = 'getCurrentArtifactStatus',
            ),

        # artifact category
        StringField(
              'xppm_response_category',
              mutator = 'setXppm_response_category',
              searchable = False,
              required = True,
              vocabulary = 'vocabulary_categories',
              widget = SelectionWidget(
                label = 'Artifact Category',
                description = 'Select new category for this artifact',
                format = 'select',
                ),
              default_method = 'getCurrentArtifactCategory',
            ),

        # the priority
        StringField(
              'xppm_response_priority',
              mutator = 'setXppm_response_priority',
              searchable = False,
              required = True,
              vocabulary = 'vocabulary_priorities',
              widget = SelectionWidget(
                  label = 'Priority',
                  description = 'Set the new priority for this artifact',
                  format = 'select',
                ),
              default_method = 'getCurrentArtifactPriority',
            ),

        # story
        StringField(
            'xppm_response_story',
            mutator = 'setXppm_response_story',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_allStoriesList',
            widget = SelectionWidget(
                  label = 'Story',
                  description = 'stories related to this artifact',
                  format = 'select',
                ),
            default_method = 'getCurrentArtifactStory',
            ),

        # attachment
        FileField(
            'xppm_response_attachment',
            widget = FileWidget(
                label = "Attachment",
                description = "You may upload a file here:",
                ),
            storage = AttributeStorage(),
            ),
        )
    )

finalizeATCTSchema(XPointResponseSchema)

#XPointResponseSchema.changeSchemataForField('

class XPointResponse(XPPMBase, ATCTContent, HistoryAwareMixin):

    schema = XPointResponseSchema

    meta_type = "XPointResponse"
    portal_type = "XPointResponse"
    archetypes_type = "XPointResponse"

    __implements__ = (HistoryAwareMixin.__implements__,
                      ATCTContent.__implements__,
                      )

    # set up the prefix for auto generated ids.
    xppm_id_prefix = 'xpr'
    # the logger.
    log = logging.getLogger("XPointProjectManagement XPointResponse")
    # preparing class security info for methods
    security = ClassSecurityInfo()

    #security.declarePublic()

    # ==================
    # get current artifact's properties and metadata.

    security.declareProtected(permissions.View, 'getCurrentArtifactStory')
    def getCurrentArtifactStory(self):
        return self.aq_inner.aq_parent.getXppm_artifact_story()

    security.declareProtected(permissions.View, 'getCurrentArtifactPriority')
    def getCurrentArtifactPriority(self):
        return self.aq_inner.aq_parent.getXppm_artifact_priority()

    security.declareProtected(permissions.View, 'getCurrentArtifactCategory')
    def getCurrentArtifactCategory(self):
        return self.aq_inner.aq_parent.getXppm_artifact_category()

    security.declareProtected(permissions.View, 'getCurrentArtifactStatus')
    def getCurrentArtifactStatus(self):
        return self.aq_inner.aq_parent.getXppm_artifact_status()

    # ==================
    # when we save a response, we need update the parent artifact with
    # the new properties and metadata, if those values are changed.

    security.declareProtected(permissions.ModifyPortalContent,
                              'setXppm_response_story')
    def setXppm_response_story(self, storyNew):
        storyNow = self.getCurrentArtifactStory()

        if storyNew and storyNow != storyNew:
            # log the story change for this artifact.
            self.logArtifactChanges("Story", storyNow, storyNew)

            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_story(storyNew)
            # update the index too.
            artifact.reindexObject(('getXppm_artifact_story', ))

        self.getField('xppm_response_story').set(self, storyNew)

    security.declareProtected(permissions.ModifyPortalContent,
                              'setXppm_response_priority')
    def setXppm_response_priority(self, priorityNew):
        priorityNow = self.getCurrentArtifactPriority()

        if priorityNew and priorityNow != priorityNew:
            self.logArtifactChanges("Priority", priorityNow,
                                    priorityNew)

            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_priority(priorityNew)
            artifact.reindexObject(('getXppm_artifact_priority', ))

        self.getField('xppm_response_priority').set(self, priorityNew)

    security.declareProtected(permissions.ModifyPortalContent,
                              'setXppm_response_category')
    def setXppm_response_category(self, categoryNew):
        categoryNow = self.getCurrentArtifactCategory()

        if categoryNew and categoryNow != categoryNew:
            self.logArtifactChanges("Category", categoryNow,
                                    categoryNew)

            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_category(categoryNew)
            artifact.reindexObject(('getXppm_artifact_catetory', ))

        self.getField('xppm_response_category').set(self, categoryNew)

    security.declareProtected(permissions.ModifyPortalContent,
                              'setXppm_response_status')
    def setXppm_response_status(self, statusNew):
        statusNow = self.getCurrentArtifactStatus()

        if statusNew and statusNow != statusNew:
            self.logArtifactChanges("Status", statusNow, statusNew)

            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_status(statusNew)
            artifact.reindexObject(('getXppm_artifact_status', ))

        self.getField("xppm_response_status").set(self, statusNew)

    def logArtifactChanges(self, name, before, after):
        artifact = self.aq_inner.aq_parent
        if not artifact._artifactChangeLog:
            artifact._artifactChangeLog = []

        # preparing the message.
        changeTime = strftime("%Y-%m-%d %H:%M:%S")

        artifact._artifactChangeLog.append({'time' : changeTime,
                                            'name' : name,
                                            'before' : before,
                                            'after' : after})
        return

# register to the plone add-on product.
registerType(XPointResponse, PROJECTNAME)