# story.py

__doc__ = """XPointStory defines a topic/module/component for a
XPointProject."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.atct import ATDocument
from Products.ATContentTypes.configuration import zconf

try: # Plone 3.0.x
    from Products.CMFCore import permissions as CMFCorePermissions
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.permissions import View

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
        # this all we need so far.
        ),
    )

# moving the keyworks selection to mail tab.
XPointStorySchema['subject'].schemata = 'default'
XPointStorySchema['subject'].required = True
XPointStorySchema['subject'].widget.label = 'Projects'
XPointStorySchema['subject'].widget.description = \
    "Select projects for this build journal, holding CTRL key to select more than one project"
XPointStorySchema['subject'].widget.size = 5
XPointStorySchema.moveField('subject', after='description')

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
    global_allow = True

    filter_content_types = True
    allowed_content_types = ('XPointTask')

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
        },)

    security = ClassSecurityInfo()

    security.declarePublic('getStoryTasks')
    def getStoryTasks(self):
      """returns all tasks in this story.
      """
      return self.contentValues(filter={'portal_type':['XPointTask']})

registerType(XPointStory, PROJECTNAME)
