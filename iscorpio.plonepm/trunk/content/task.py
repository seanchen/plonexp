# task.py

__doc__ = """XPointTask defines the task for a XPointStory
journal."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import IntDisplayList
from Products.Archetypes.public import registerType
# from ATContentType
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.configuration import zconf

from Products.CMFCore.utils import getToolByName
try: # Plone 3.0.x
    from Products.CMFCore import permissions as CMFCorePermissions
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.permissions import View

from Products.XPointProjectManagement.config import *

# the schema for XPointTask.
XPointTaskSchema = ATFolderSchema.copy() + Schema((

        # text field for details description for this task.
        TextField(
            'task_text',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Task description',
                description = 'Provide the detail descrpiton for your task',
                rows = 25,
                ),
            ),

        # estimated hours for this task.
        IntegerField(
            'task_estimated_hours',
            searchable = False,
            required = False,
            widget = IntegerWidget(
                label = 'Estimated Hours',
                descrpiton = 'Put here the estimated hours for this task',
                ),
            ),

        # Progress Status in percentage. 0% - 100%
        IntegerField(
            'task_progress_percent',
            searchable = False,
            required = True,
            default = 0,
            # set the range from 0 to 100
            vocabulary = IntDisplayList([(i, i) for i in range(0, 101)]),
            widget = SelectionWidget(
                label = 'Progress Status',
                descrpiton = 'Progress status in percentage 0% - 100%',
                format = 'select',
                ),
            ),

        # owner of this task.??? select from membership.
        # getToolByName(self, 'portal_membership')
        LinesField(
            'task_owners',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_allMembersList',
            widget = InAndOutWidget(
                label = 'Task Owner(s)',
                descrpiton = "Please select owners for this task",
                ),
            ),
        ),
    )

# set the description field to invisible, we are not going to use it
# for a task.
XPointTaskSchema['description'].widget.visible = False

# make the related item visible and move to the bottom.
XPointTaskSchema['relatedItems'].widget.visible = True
XPointTaskSchema['relatedItems'].widget.description = \
    "Select related tasks"
XPointTaskSchema.moveField('relatedItems', pos='bottom')

# the content type class.
class XPointTask(ATFolder):
    """The ATConentType class for a XPointTask.
    """

    schema = XPointTaskSchema

    # type name and defination
    meta_type = 'XPointTask'
    portal_type = 'XPointTask'
    # this will show on the page.
    archetype_name = 'XP Task'

    content_icon = 'XPTask_icon.gif'
    immediate_view = 'xpointtask_view'
    default_view = 'xpointtask_view'

    _at_rename_after_creation = True
    global_allow = False

    filter_content_types = True
    allowed_content_types = ('XPointMemo',)

    actions = ({
        'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/xpointtask_view',
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

# register this type.
registerType(XPointTask, PROJECTNAME)
