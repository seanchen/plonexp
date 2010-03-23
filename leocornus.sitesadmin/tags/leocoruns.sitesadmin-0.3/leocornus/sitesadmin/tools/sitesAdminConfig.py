
# config.py

"""
Sites Admin configlet in control panel.
"""

from zope.component import getUtility
from zope.component import adapts
from zope.interface import implements
from zope.formlib.form import FormFields
from zope.schema.fieldproperty import FieldProperty

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm

from interfaces import ISitesAdminConfig

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the form class
class SitesAdminConfigForm(ControlPanelForm):

    form_fields = FormFields(ISitesAdminConfig)

    label = u"Configuration Panel for Sites Admin"
    description = u'This panel will be used to config'

    form_name = u'Hide Unnessary Add-on Products'

# sitesadmim property sheet is used for property storage.
class SitesAdminConfigAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISitesAdminConfig)

    def __init__(self, context):
        super(SitesAdminConfigAdapter, self).__init__(context)
        properties = getToolByName(self.context,
                                   'portal_properties')
        self.props = getattr(properties, 'sitesadmin_properties')

    def get_productsNotToList(self):

        return '\n'.join(self.props.getProperty('productsNotToList'))

    def set_productsNotToList(self, value):

        self.props.manage_changeProperties(productsNotToList=value.split('\n'))

    productsNotToList = property(get_productsNotToList, set_productsNotToList)

