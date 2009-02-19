# Install.py

from Products.CMFCore.utils import getToolByName
from Products.CMFFormController.FormAction import FormActionKey
from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.public import listTypes

from StringIO import StringIO

from Products.CMFDynamicViewFTI.migrate import migrateFTIs

from Products.XPointProjectManagement.config import *

# When the installation is executed by "Add/Remove Products" on Plone UI, 
# this function is called. 
# Here, you may do the following: Skin/CSS/JavaScript registration, 
# PortalFacotry registration, content type conversion to DynamicViewFTI, 
# etc.
def install(self):
    """Install XPointProjectManagement"""

    # Because return value of this function becomes an 
    # installation log, StringIO is taken out temporarily outputting to 
    # the buffer, and bringing it together later instead of a standard 
    # output.
    out = StringIO()

    # The installation beginning log is output first. 
    print >> out, "Installing %s" % PROJECTNAME

    # It is made to use with Plone by registering the contents type. The 
    # listTypes function returns the list of the class object registered 
    # with registerType(). Information registered here can be confirmed 
    # and be changed with plone/portal_types. Moreover, when these 
    # parameters are changed on the product code because parameters such 
    # as global_allow and default_view are preserved in this 
    # plone/portal_types, it is necessary to add the product again to 
    # update the setting. 
    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    print >> out, "Installed types"


    # Migrate FTI, to make sure we get the necessary infrastructure for 
    # the 'display' menu to work on Plone UI. Two or more View can be 
    # originally prepared in the contents type newly made though View of 
    # the folder includes the photograph list etc in the Plone standard. 
    # Please refer to suppl_views of the contents type mounting class for 
    # the specification method.
    migrated = migrateFTIs(self, product=PROJECTNAME)
    print >>out, "Switched to DynamicViewFTI: %s" % ', '.join(migrated)

    # When the instance of contents is newly made, the instance is made 
    # in a temporary area when portal_factory is made effective. When the 
    # save button is pushed, the instance is moved to an actual folder. 
    # When this mechanism is used, it doesn't remain in the folder from 
    # which remains of the instance left while making it are open to the 
    # public in general.
    factory = getToolByName(self, 'portal_factory')
    types = factory.getFactoryTypes().keys()
    for add_type in ('XPointBuildJournal',):
        if add_type not in types:
            types.append(add_type)
            factory.manage_setPortalFactoryTypes(listOfTypeIds = types)

    print >> out, "Added %s to portal_factory" % PROJECTNAME

    # Resources (as css and JavaScript, etc.) is installed. Because the 
    # composition was different in each product, it made it to another 
    # function.
    install_resources(self, out)

    # The installation log is returned.
    return out.getvalue()


# Resources (css and JavaScript, etc.) is installed.
def install_resources(self, out):
    # 'install_subskin' adds the layer of ATCTSmallSample to the skin 
    # selection of portal_skins. An additional position of the layer 
    # becomes it next to 'custom'.
    install_subskin(self, out, GLOBALS)
    print >> out, "Installed skin"

    # The plone/portal_css instance is acquired. 
    portal_css = getToolByName(self, 'portal_css')

    # CSS is registered in portal_css. Because the TAL expression can be 
    # described in expression, a flexible use condition judgment in the 
    # mechanism of Plone can be specified. When portal_type is checked or 
    # a complex check is necessary for the TAL expression, the Python 
    # script for the check can be called. CSS registered in portal_css 
    # need not write the code for uninstall because it is automatically 
    # deleted when this product is uninstalled (For Plone-2.1.2).
    portal_css.manage_addStylesheet(# Object name to registration.
                                    id = 'xpointc.css',
                                    # TAL expression for using condition
                                    expression = '',
                                    # browser media type
                                    media = 'all',
                                    # Title for portal_css
                                    title = 'inline xpointx styles',
                                    # initial available status.
                                    enabled = True)

    print >> out, "Installed css"

# When uninstallation is executed by "Add/Remove Products" on Plone UI, 
# it is called. Processing for which the 
# registration release is necessary is done here.
def uninstall(self):
    # The buffer is made as well as the install time at the output 
    # destination of the uninstallation log.
    out = StringIO()

    # The uninstallation processing of resources is called.
    uninstall_resources(self, out)

    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()


# The uninstallation processing of resources is done.
def uninstall_resources(self, out):
    """Remove the js and css files from the resource registries"""

    # The skin's uninstallation processing is called.
    uninstallSkins(self, out)

    print >>out, "Resource files removed"


# The uninstallation processing of skins is done.
def uninstallSkins(self, out):
    # The plone/portal_skins instance is acquired. 
    skins_tool = getToolByName(self, 'portal_skins')

    # The list of skin selections is acquired. 'Plone Default' and 'Plone 
    # Tableless' are acquired in the standard of Plone.
    skins = skins_tool.getSkinSelections()

    # The deletion processing of the ATCTSmallSample layer is done in 
    # each skin selection.
    for skin in skins:
        # The layer list in the skin selection is acquired.
        path = skins_tool.getSkinPath(skin)

        # An extra blank in the back and forth is removed by dividing by 
        # the comma because the layer list is string type of the comma 
        # district switching off. 
        path = [p.strip() for p in path.split(',') if p]

        # Processing that removes the element is repeated while there is 
        # a corresponding element to PROJECTNAME in the list of path.
        while PROJECTNAME in path:
            # The element is removed in the list. Because PROJECTNAME is 
            # removed here, it is assumed that there is a directory of 
            # the same name as config.PROJECTNAME below the skins 
            # directory. Therefore, it is not removed in this processing 
            # when two or more skin directories are in skins or less.
            path.remove(PROJECTNAME)

        # The layer list that removes the skin layer of ATCTSmallSample 
        # is connected with the character string of the comma district 
        # switching off and it preserves it.
        skins_tool.addSkinSelection(skin, ','.join(path))

    print >> out, "Uninstalled skin"
