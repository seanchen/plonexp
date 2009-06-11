# config.py

from zope.component import getUtility
from zope.component import adapts
from zope.interface import implements
from zope.formlib.form import FormFields
from zope.schema.fieldproperty import FieldProperty
from zope.i18nmessageid import MessageFactory

from OFS.SimpleItem import SimpleItem

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm

from interfaces import ISillyConfiguration

_ = MessageFactory('iscorpio.plonelab')

# the form class
class SillyConfigurationForm(ControlPanelForm):

    form_fields = FormFields(ISillyConfiguration)

    label = _(u"A silly settings form")
    description = _(u'Put details description here!')

    form_name = _(u'Section Name',
                  default=u'Attributes')

class SillyConfigurationAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISillyConfiguration)

    def __init__(self, context):
        super(SillyConfigurationAdapter, self).__init__(context)
        self.tool = getToolByName(self.context,
                                  'iscorpio_plonelab')

    def get_favorite_color(self):

        return self.tool.favorite_color

    def set_favorite_color(self, value):

        self.tool.favorite_color = value

    favorite_color = property(get_favorite_color, set_favorite_color)

# the utility class to do storage.
class SillyConfiguration(SimpleItem):

    implements(ISillyConfiguration)

    favorite_color = FieldProperty(ISillyConfiguration['favorite_color'])
    #contact_email = FieldProperty(ISillyConfiguration['contact_email'])

def form_adapter(context):

    return getUtility(ISillyConfiguration, name="silly_config",
                      context=context)
    
