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
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import LinesWidget
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
        # developers for this project
        LinesField(
            'project_developers',
            searchable = False,
            required = True,
            vocabulary = 'vocabulary_allMembersList',
            widget = InAndOutWidget(
                label = 'Developers',
                descrpiton = "Please select developers for this project",
                ),
            ),
        # modules
        LinesField(
            'project_modules',
            searchable = False,
            required = True,
            widget = LinesWidget(
                label = 'Project Modules',
                description = 'Please specify the module for your project, one per line',
                cols = 40,
                ),
            ),
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
    default_view = 'xpointproject_release_view'

    _at_rename_after_creation = True
    global_allow = True

    # restrict allowed content types.
    filter_content_types = True
    allowed_content_types = ('XPointStory', 'XPointRelease', 'Topic')

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

    #security.declareProtected('vocabulary_allMembersList')
    def vocabulary_allMembersList(self):
        """ Return a list of tuple (user_id, fullname, email) for all
        the members of the portal.
        """
        members = []
        portalMembers = getToolByName(self, 'portal_membership')
        members = [(member.id,
                    member.getProperty('fullname',None),
                    member.getProperty('email',None))
                   for member in portalMembers.listMembers()]

        return DisplayList(members)

    security.declarePublic('getProjectDevelopers')
    def getProjectDevelopers(self):
        """ returns all developers for this project.
        """
        return self.getProject_developers()

    security.declarePublic('getProjectModules')
    def getProjectModules(self):
        """ returns all modules for this project.
        """
        return self.getProject_modules()

    security.declarePublic('getProjectReleases')
    def getProjectReleases(self):
        """ returns all releases defined in this project.
        """
        # order sub-objects by id and reverse.
        #self.orderObjects(self.id, reverse=True)
        return self.contentValues(
            filter = {'portal_type':['XPointRelease']}
            )

    security.declarePublic('getProjectRelease')
    def getProjectRelease(self, releaseId):
        """ return the release notes for the specified release id.
        """
        for release in self.getProjectReleases():
            if release.id == releaseId:
                return release

        return None

    security.declarePublic('getProjectPublishedReleases')
    def getProjectPublishedReleaseIds(self):
        """ returns a list of published release ids.
        """
        projectReleases = self.getProjectReleases()
        if projectReleases:
            wtool = getToolByName(self, 'portal_workflow')
            releaseIds = []
            for release in self.getProjectReleases():
                if wtool.getInfoFor(release, 'review_state') == 'published':
                    releaseIds.append(release.id)
    
            releaseIds.sort()
            releaseIds.reverse()
            return releaseIds
        else:
            return None

    security.declarePublic('getProjectStories')
    def getProjectStories(self):
        """ returns all stories in this project.
        """
        return self.contentValues(
            filter = {'portal_type': ['XPointStory']}
            )

    security.declarePublic('getModuleStories')
    def getModuleStories(self, moduleName):
        """ return all stories for a module.
        """
        stories = []
        for story in self.getProjectStories():
            if story.getStory_module() == moduleName:
                stories.append(story)

        return stories

    security.declarePublic('getReleaseStories')
    def getReleaseStories(self, releaseId):
        """ return all stories for the given release.
        """
        stories = []
        for story in self.getProjectStories():
            if releaseId in story.getStory_releases():
                stories.append(story)

        return stories

    security.declarePublic('getProjectTasks')
    def getProjectTasks(self):
        """ return all tasks of this project, order by completion date.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = '/'.join(self.getPhysicalPath())
        query = {
            'portal_type':['XPointTask'],
            'sort_on':'getTask_completion_date',
            'sort_order':'reverse',
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

    security.declarePublic('getProjectImps')
    def getProjectImps(self):
        """ return all imps for this project, order by modification date.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = '/'.join(self.getPhysicalPath())
        query = {
            'portal_type':['XPointMemo', 'XPointIssue', 'XPointProposal'],
            'sort_on':'Date',
            'sort_order':'reverse',
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

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
            'sort_on':'Date',
            'sort_order':'reverse',
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

    security.declarePublic('getTasksForMember')
    def getTasksForMember(self, memberId=''):
        """ Returns all tasks for the specified member id.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = '/'.join(self.getPhysicalPath())
        query = {
            'portal_type':['XPointTask'],
            'getTask_owners':memberId,
            'sort_on':'getTask_completion_date',
            'sort_order':'reverse',
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

    security.declarePublic('getImpsForMember')
    def getImpsForMember(self, memberId=''):
        """ Returns all responsed for the specified member id.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = '/'.join(self.getPhysicalPath())
        query = {
            'portal_type':['XPointMemo', 'XPointIssue', 'XPointProposal'],
            'Creator':memberId,
            'sort_on':'Date',
            'sort_order':'reverse',
            'path':cpath,
            }

        return portal_catalog.searchResults(query)

# register to the plone add-on product.
registerType(XPointProject, PROJECTNAME)
