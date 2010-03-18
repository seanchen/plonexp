
# user.py

"""
Here, we will define the user account managed by membrane.
"""

from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import PasswordWidget
from Products.Archetypes.public import registerType
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.public import TextField
from Products.Archetypes.public import TextAreaWidget

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent

from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import IUserAuthentication
from Products.membrane.interfaces import IPropertiesProvider
from Products.membrane.interfaces import IGroupsProvider
from Products.membrane.interfaces import IUserRoles
from Products.membrane.interfaces import IGroupAwareRolesProvider
from Products.membrane.utils import getFilteredValidRolesForPortal

from leocornus.sitesadmin.config import PROJECTNAME
from leocornus.sitesadmin.interfaces import IUserAccount

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

UserAccountSchema = ATCTContent.schema.copy() + Schema((

    StringField(
        'userName',
        required = True,
        languageIndependent = 1,
        widget = StringWidget(
            label = "User Login Name",
            description = "User's login name, which is used for sign on."
            ),
        ),

    StringField(
        'password',
        languageIndependent = 1,
        widget = PasswordWidget(
            label = "Password",
            description = "User's Password.",
            ),
        ),

    StringField(
        'fullname',
        languageIndependent = 1,
        required = True,
        user_property=True,
        widget = StringWidget(
            label = "Full Name",
            description = "User's Full name."
            ),
        ),

    StringField(
        'email',
        languageIndependent = 1,
        required = True,
        user_property=True,
        widget = StringWidget(
            label="Email Address",
            description = "User's Email Address."
            ),
        ),

    TextField(
        'description',
        user_property=True,
        widget = TextAreaWidget(
            label = "Biography",
            description = "A short overview of who you are and what you do. Will be displayed on the your author page, linked from the items you create."
            ),
        ),

    StringField(
        'location',
        languageIndependent = 1,
        user_property=True,
        widget = StringWidget(
            label="Location",
            description = "User's Location."
            ),
        ),

    StringField(
        'home_page',
        languageIndependent = 1,
        user_property=True,
        widget = StringWidget(
            label="Home Page",
            description = "User's Home Page."
            ),
        ),

    StringField(
        'wysiwyg_editor',
        languageIndependent = 1,
        user_property=True,
        widget = StringWidget(
            label="Content Editor",
            description = "Select the content editor that you would like to use."
            ),
        ),

    LinesField(
        'sites',
        languageIndependent = 1,
        user_property=True,
        widget = LinesWidget(
            label = "Sites",
            description = "How user associate with sites",
            ),
        ),
 
    LinesField(
        # not 'roles' b/c 'validate_roles' exists; stoopid Archetypes
        name="roles_",
        accessor='getRoles',
        mutator='setRoles',
        languageIndependent=1,
        vocabulary='getRoleSet',
        multiValued=1,
        widget=MultiSelectionWidget(
            label="Roles",
            description="Roles that member has.",
            modes = (),
            ),
        ),
    ))

finalizeATCTSchema(UserAccountSchema)

# tweak the field loacation
UserAccountSchema.changeSchemataForField('location', 'default')

#UserAccountSchema['roles_'].widget.visible['edit'] = 'hidden'
#UserAccountSchema['description'].widget.visible['edit'] = 'invisible'
# hide all fields for settings
UserAccountSchema['allowDiscussion'].widget.visible['edit'] = 'invisible'
UserAccountSchema['excludeFromNav'].widget.visible['edit'] = 'invisible'
# hide fields for dates
UserAccountSchema['effectiveDate'].widget.visible['edit'] = 'invisible'
UserAccountSchema['expirationDate'].widget.visible['edit'] = 'invisible'
# hide fields from ownership
UserAccountSchema['creators'].widget.visible['edit'] = 'invisible'
UserAccountSchema['contributors'].widget.visible['edit'] = 'invisible'
UserAccountSchema['rights'].widget.visible['edit'] = 'invisible'
# hide fields from categorization
UserAccountSchema['relatedItems'].widget.visible['edit'] = 'invisible'
UserAccountSchema['language'].widget.visible['edit'] = 'invisible'

class UserAccount(ATCTContent):
    """
    A simple member archetype
    """

    schema = UserAccountSchema

    # type, name
    meta_type = 'UserAccount'
    portal_type = 'UserAccount'
    archetype_name = 'UserAccount'

    _at_rename_after_creation = True

    __implements__ = (ATCTContent.__implements__)

    security = ClassSecurityInfo()

    implements(IUserAccount,
               IUserAuthProvider, IUserAuthentication,
               IPropertiesProvider, IGroupsProvider,
               IGroupAwareRolesProvider, IUserRoles)

    getRoleSet = getFilteredValidRolesForPortal

    #
    # IUserAuthentication implementation
    # 'getUserName' is auto-generated
    #
    def verifyCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')

        if login == self.getUserName():
            # it is a membrane user.
            if login.find('\\') < 0:
                # non-ops users
                if password == self.getPassword():
                    return True
            elif login.startswith('ext\\'):
                # non-ops users.
                if password == self.getPassword():
                    return True
            else:
                # verify through ldap plugin.
                userFolder = getToolByName(self, 'acl_users')
                return userFolder.sitesadmin_proxy.verifyCredentials(credentials)
        else:
            # query the LDAP.
            # XXX Not support now!
            return False

    #
    # IUserRoles implementation
    # 'getRoles' is autogenerated

registerType(UserAccount, PROJECTNAME)
