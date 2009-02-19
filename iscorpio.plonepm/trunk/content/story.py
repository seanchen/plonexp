# story.py

__doc__ = """XPointStory defines a topic/module/component for a
XPointProject."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.configuration import zconf

try: # Plone 3.0.x
    from Products.CMFCore import permissions as CMFCorePermissions
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName

# the configruation info for this project.
from Products.XPointProjectManagement.config import *

# define the schem for this content type.
# a XPointStory is a folder in Plone site.
XPointStorySchema = ATFolderSchema.copy() + Schema((

        # we need a rich text body for the story.
        TextField(
            'story_text',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Story body',
                description = 'Provide details description for your story',
                rows = 22,
                ),
            ),

        # the module for this tory.
        StringField(
            'story_module',
            searchable = False,
            required = True,
            vocabulary = 'getProjectModules',
            default = 'mosapp',
            widget = SelectionWidget(
                label = "Module",
                description = "Select the module for this story",
                format = 'select'
                ),
            ),

        # select the release that this story will be included.
        LinesField(
            'story_releases',
            searchable = True,
            required = True,
            vocabulary = 'vocabulary_releases',
            widget = InAndOutWidget(
                label = 'Planned Releases',
                description = 'Select planned releases for this story',
                ),
            ),
        ),
    )

# we don't need description here.
XPointStorySchema['description'].widget.visible = False
# make this related items field visible and move to bottom.
XPointStorySchema['relatedItems'].widget.visible = True
XPointStorySchema['relatedItems'].widget.description = \
    "Select related items"
XPointStorySchema.moveField('relatedItems', pos='bottom')

# the XPointStory class.
class XPointStory(ATFolder):
    """XPoint Story for a XPointProject"""

    schema = XPointStorySchema

    # type name and defination
    meta_type = 'XPointStory'
    portal_type = 'XPointStory'
    archetype_name = 'XP Story'

    content_icon = 'XPStory_icon.gif'
    immediate_view = 'xpointstory_view'
    default_view = 'xpointstory_view'

    _at_rename_after_creation = True
    global_allow = False

    filter_content_types = True
    allowed_content_types = ('XPointTask', 'XPointMemo',
                             'XPointIssue', 'XPointProposal')

    allow_discussion = True

    # for logging.
    log = logging.getLogger("XPointProjectManagement Story")

    actions = ({
        'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/xpointstory_view',
        'permissions': (CMFCorePermissions.View,)
        },{
        'id': 'edit',
        'name': 'Edit',
        'action': 'string:${object_url}/base_edit',
        'permissions': (CMFCorePermissions.ViewManagementScreens,)
        },{
        'id': 'metadata',
        'name': 'Properties',
        'action': 'string:${object_url}/base_metadata',
        'permissions': (CMFCorePermissions.ViewManagementScreens,)
        },{
        'id': 'local_roles',
        'name': 'Sharing',
        'action': 'string:${object_url}/sharing',
        'permissions': (CMFCorePermissions.ViewManagementScreens,)
        })

    security = ClassSecurityInfo()

    def vocabulary_releases(self):
        """ Return all available releases for this story.
        """
        releases = []
        for release in self.getProjectReleases():
            releases.append((release.id, release.title))

        return DisplayList(releases)

    security.declarePublic('getStoryEstimatedHours')
    def getStoryEstimatedHours(self):
        """ returns the subtotal of the estimated hours for all tasks.
        """

        tasks = self.getStoryTasks()
        estimatedSubtotal = 0
        for task in tasks:
            # calc the subtotal of estimated hours.
            if task.getTask_estimated_hours != None:
                self.log.debug("Estimated hours [%s] for task [%s]",
                               task.task_estimated_hours, task.id)
                estimatedSubtotal = estimatedSubtotal + task.task_estimated_hours

        return estimatedSubtotal

    security.declarePublic('getStoryProgressPercent')
    def getStoryProgressPercent(self):
        """ returns the progress percent for this story, it should be the
        progress average of all its task.
        """

        tasks = self.getStoryTasks()
        averageProgress = 0
        if len(tasks) > 0:
            progressSubtotal = 0
            for task in tasks:
                # calc the subtotal ...
                if task.getTask_progress_percent != None:
                    self.log.debug("Progress percent [%s] for task [%s]",
                                   task.task_progress_percent, task.id)
                    progressSubtotal = progressSubtotal + task.task_progress_percent

            # calc the average.
            averageProgress = progressSubtotal / len(tasks)

        return averageProgress

    security.declarePublic('getStoryTasks')
    def getStoryTasks(self):
      """ returns all tasks in this story.
      """
      return self.contentValues(
          filter = {
              'portal_type':['XPointTask']
              }
          )

    security.declarePublic('getStroyMemosIssuesProposals')
    def getStoryMemosIssuesProposals(self):
        """ return all memos for this story, should includes all tasks' memo.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = '/'.join(self.getPhysicalPath())
        query = {
            'portal_type':['XPointMemo', 'XPointIssue', 'XPointProposal',],
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

registerType(XPointStory, PROJECTNAME)
