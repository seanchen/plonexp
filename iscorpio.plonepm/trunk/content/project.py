# project.py

__doc__ = """XPointProject defines a software project."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
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

# define a XPointProject as a folder in plone site.
XPointProjectSchema = ATFolderSchema.copy() + Schema((

        # detail description for this project, it allows rich text.
        TextField(
            'project_text',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Project body',
                description = 'Provide details description for your project',
                rows = 22,
                ),
            ),

        # anything else?
        )
    )

# customizing the schema here, set visible of some fields, location of
# some fields.

# make this related items field visible and move to bottom.
XPointProjectSchema['relatedItems'].widget.visible = True
XPointProjectSchema['relatedItems'].widget.description = \
    "Select related items"
XPointProjectSchema.moveField('relatedItems', pos='bottom')

# here is the class.
class XPointProject(ATFolder):
    """XPointProject defines a software project following eXtreme
    Programming's idea/concept.
    """

    schema = XPointProjectSchema

    # type, name
    meta_type = 'XPointProject'
    portal_type = 'XPointProject'
    archetype_name = 'XP Project'

    content_icon = 'XPProject_icon.gif'
    # view.
    immediate_view = 'xpointproject_view'
    default_view = 'xpointproject_view'

    _at_rename_after_creation = True
    global_allow = True

    # restrict allowed content types.
    filter_content_types = True
    allowed_content_types = ('XPointStory', 'Topic')

    # the logger.
    log = logging.getLogger("XPointProjectManagement Project")

    actions = ({
        'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/xpointproject_view',
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
        },)

    # preparing class security info for methods.
    security = ClassSecurityInfo()

    security.declarePublic('getProjectStories')
    def getProjectStories(self):
        """ returns all stories in this project.
        """
        return self.contentValues(filter={'portal_type': ['XPointStory']})

    security.declarePublic('getProjectEstimatedHours')
    def getProjectEstimatedHours(self):
        """ returns the amount of hours estimated for this project.
        """

        stories = self.getProjectStories()
        hours = 0
        for story in stories:
            hours = hours + story.getStoryEstimatedHours()

        return hours

    security.declarePublic('getProjectProgressPercent')
    def getProjectProgressPercent(self):
        """ returns the progress status as a percentage for this project. 
        """

        stories = self.getProjectStories()
        progressPercent = 0
        if len(stories) > 0:
            progress = 0
            for story in stories:
                progress = progress + story.getStoryProgressPercent()

            progressPercent = progress / len(stories)

        return progressPercent

    security.declarePublic('getOutstandingIssues')
    def getOutstandingIssues(self):
        """ returns issues with status open and pending.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = '/'.join(self.getPhysicalPath())
        query = {
            'portal_type':['XPointIssue'],
            'getXpoint_tracking_status':['open','pending',],
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

    security.declarePublic('getProjectDevelopers')
    def getProjectDevelopers(self):
        """ returns all developers for this project.
        """
        portal_catalog = getToolByName(self, 'portal.catalog')
        return portal_catalog.uniqueValuesFor('getTask_owners')

    security.declarePublic('getTasksForMember')
    def getTasksForMember(self, memberId=''):
        """ Returns all tasks for the specified member id.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = '/'.join(self.getPhysicalPath())
        query = {
            'portal_type':['XPointTask'],
            'getTask_owners':memberId,
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

# register to the plone add-on product.
registerType(XPointProject, PROJECTNAME)
