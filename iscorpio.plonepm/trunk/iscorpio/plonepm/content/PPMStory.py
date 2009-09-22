
# PPMStory.py

__doc__ = """PPMStory defines a story for a software project in Agile approach."""
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
from Products.Archetypes.public import IntDisplayList
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.FixedColumn import FixedColumn

from Products.CMFCore.utils import getToolByName

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase

__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'

# the schema for story.
PPMStorySchema = ATFolderSchema.copy() + Schema((

        # scope details
        TextField(
            'text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Details',
                description = 'Details description for this story',
                rows = 18,
                ),
            ),

        # 
        DataGridField(
            'xppm_time_tracking',
            searchable = False,
            required = False,
            columns = ('date', 'desc', 'hours'),
            allow_empty_rows = False,
            allow_insert = True,
            allow_reorder = False,
            allow_delete = False,
            widget = DataGridWidget(
                label = u'Story Time Tracking',
                auto_insert = True,
                description = "Tracking time spent on this story",
                columns = {
                    'date' : FixedColumn("Date"),
                    'desc' : Column("Description"),
                    'hours' : Column("Hours")
                    },
                ),
            ),

        # planned completed date, 90% finish deadline
        DateTimeField(
            'xppm_completion_date',
            searchable = False,
            required = True,
            widget = CalendarWidget(
                label = '90% Completion Deadline',
                description = 'Specify the date when this task should be completed at less 90%',
                starting_year = 2007,
                show_hm = False,
                ),
            schemata = 'Manage',
            ),

        # Progress Status in percentage. 0% - 100%
        IntegerField(
            'xppm_story_progress_percent',
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
            schemata = 'Manage',
            ),

        # estimated hours for this task.
        IntegerField(
            'xppm_story_estimated_hours',
            searchable = False,
            required = False,
            widget = IntegerWidget(
                label = 'Estimated Hours',
                descrpiton = 'Put here the estimated hours for this task',
                ),
            schemata = 'Manage',
            ),

        # used hours for this task.
        IntegerField(
            'xppm_story_used_hours',
            searchable = False,
            required = False,
            widget = IntegerWidget(
                label = 'Actual Used Hours',
                descrpiton = 'Put here the actual used hours for this task',
                ),
            schemata = 'Manage',
            ),

        # owner of this task.??? select from membership.
        # getToolByName(self, 'portal_membership')
        LinesField(
            'xppm_story_owners',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_developers',
            widget = InAndOutWidget(
                label = 'Task Owner(s)',
                descrpiton = "Please select owners for this task",
                ),
            schemata = 'Manage',
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
            schemata = 'Manage',
            ),

        # system requirements list.
        LinesField(
            'xppm_story_sysreqs',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_allSysreqsList',
            widget = InAndOutWidget(
                label = 'System Requirements',
                description = 'Please select system requirements for your story',
                ),
            schemata = 'Manage',
            ),
        ),
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

        #security.declareProtected('vocabulary_allMembersList')
    def vocabulary_developers(self):
        """ Return a list of tuple (user_id, fullname, email) for all
        the members of the portal.
        """
        members = []
        portalMembers = getToolByName(self, 'portal_membership')
        developers = self.getProjectDevelopers()
        for memberId in developers:
            members.append((memberId,
                            portalMembers.getMemberById(memberId).getProperty('fullname', None))
                           )

        return DisplayList(members)

# register to the plone add-on product.
registerType(PPMStory, PROJECTNAME)
