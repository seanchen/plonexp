
# XPointProject.py

__doc__ = """XPointProject defines a software project in Agile approach."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
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
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.configuration import zconf

from Products.CMFCore.utils import getToolByName

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME

# define a XPointProject as a folder in plone site.
XPointProjectSchema = ATFolderSchema.copy() + Schema((

        # detail description for this project, it allows rich text.
        TextField(
            'xppm_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Project body',
                rows = 22,
                ),
            ),

        # developers for this project
        LinesField(
            'xppm_developers',
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
            'xppm_modules',
            searchable = False,
            required = True,
            widget = LinesWidget(
                label = 'Project Modules',
                description = 'Please specify the module for your project, one per line',
                cols = 40,
                ),
            ),

        # the unique sequence will serve
        IntegerField(
            'xppm_unique_sequence',
            default = 0,
            # hide for view mode.
            widget = IntegerWidget(
                label = 'Unique Sequence',
                description = 'This sequence will generate unique ids for all artifacts in this project.',
                ),
            ),
        )
    )

finalizeATCTSchema(XPointProjectSchema)

# customizing the schema here, set visible of some fields, location of
# some fields.
XPointProjectSchema.changeSchemataForField('xppm_unique_sequence', 'settings')

# here is the class.
class XPointProject(ATFolder):
    """XPointProject defines a software project following eXtreme
    Programming's idea/concept.
    """

    schema = XPointProjectSchema

    # type, name
    meta_type = 'XPointProject'
    portal_type = 'XPointProject'
    archetype_name = 'XPointProject'

    _at_rename_after_creation = True

    # the logger.
    log = logging.getLogger("PlonePM Project")

    # preparing class security info for methods.
    security = ClassSecurityInfo()

    security.declarePublic('getNextUniqueId')
    def getNextUniqueId(self):
        """ Return the next value from the unique sequence, and
            update the sequence itself.
        """
        newId = self.xppm_unique_sequence + 1
        self.setXppm_unique_sequence(newId)
        return newId

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

    #security.declarePublic('vocabulary_allStoriesList')
    def vocabulary_allStoriesList(self):
        """ Returns a display list for all stories, the format is like this:
        [id, id + title].
        """
        retList = []
        stories = self.getAllStories()
        for story in stories:
            retList.append((story.id, story.id + ' ' + story.Title))

        self.log.debug('we got %s stories', len(retList))
        return DisplayList(retList)

    security.declarePublic('getProjectDevelopers')
    def getProjectDevelopers(self):
        """ returns all developers for this project.
        """
        return self.getXppm_developers()

    security.declarePublic('getAllStories')
    def getAllStories(self):
        """ Return all Stories in this project.
        """
        return self.xpCatalogSearch(portal_type='XPointStory')

    security.declarePublic('getAllSysReqs')
    def getAllSysReqs(self):
        """ Return all system requirement in this project.
        """
        return self.xpCatalogSearch(portal_type='XPointSysReq')

    security.declarePublic('getMetadataByType')
    def getMetadataByType(self, type=None):
        """ this will return a catalog search result based on the
        given metadata type.
        """
        if type is None:
            return []

        query = {}
        query['portal_type'] = 'XPointMetadata'
        query['getXppm_metadata_type'] = type

        metadata = [(one.id, one.Title) for one in self.xpCatalogSearch(query)]
        self.log.debug("Metadata for type %s: %s", type, metadata)
        return metadata

    security.declarePublic('getMetadataById')
    def getMetadataById(self, theId):
        """ return an unique metadata by the given id.
        """
        query = {'id' : theId}
        oneMetadata = self.xpCatalogSearch(query)[0]
        return oneMetadata

    security.declarePublic('xpCatalogSearch')
    def xpCatalogSearch(self, criteria=None, **kwargs):
        """ returns the catalog search result based on the provided criteria
        or kwargs.
        """

        if criteria is None:
            criteria = kwargs
        else:
            criteria = dict(criteria)

        availableCriteria = {'id' : 'getId',
                             'text' : 'SearchableText',
                             'portal_type' : 'portal_type',
                             'metadata_type' : 'getXppm_metadata_type',
                             }

        query = {}
        query['path'] = '/'.join(self.getPhysicalPath())

        for k, v in availableCriteria.items():
            if k in criteria:
                query[v] = criteria[k]
            elif v in criteria:
                query[v] = criteria[v]

        query['sort_on'] = 'created'
        #query['sort_order'] = 'reverse'

        catalog = getToolByName(self, 'portal_catalog')

        return catalog.searchResults(query)

# register to the plone add-on product.
registerType(XPointProject, PROJECTNAME)
