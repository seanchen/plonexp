# permissions.py

from AccessControl import ModuleSecurityInfo
from AccessControl import Permissions

from Products.CMFCore import permissions as CMFCorePermissions
import Products.Archetypes.public as atapi

import config

# initializing the permissions for the product: define the permission
# name and set the default roles for each permission.
# Normally, the name will be something like ProjectName: Add ContentTypeName
def initialize():

    # the permission dict for all content types in this project.
    # What we are trying to do here is adding a "Add" permission for
    # each content type, and assigning default roles for this
    # permission to 'Manager' and 'Owner'.
    # We do NOT have to do this.  We are free to add whatever
    # permission with whatever name (Of course, with some convention
    # on the name, it is much easier to management).
    permissions = {}

    # get all content types within this project.
    types = atapi.listTypes(config.PROJECTNAME)

    for aType in types:

        permission = '%s: Add %s' % (config.PROJECTNAME,
                                     aType['portal_type'])
        permissions[aType['portal_type']] = permission

        # the setDefaultRoles method will also add this new permission
        # to the Plone site.
        CMFCorePermissions.setDefaultRoles(permission,
                                           ('Manager', 'Owner'))

    return permissions
