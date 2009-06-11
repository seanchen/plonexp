# config.py

from zope.component import getUtility
from zope.interface import implements
from zope.formlib.form import FormFields
from zope.schema.fieldproperty import FieldProperty
from zope.i18nmessageid import MessageFactory

from OFS.SimpleItem import SimpleItem

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

# the utility class to do storage.
class SillyConfiguration(SimpleItem):

    implements(ISillyConfiguration)

    favorite_color = FieldProperty(ISillyConfiguration['favorite_color'])
    #contact_email = FieldProperty(ISillyConfiguration['contact_email'])

def form_adapter(context):

    return getUtility(ISillyConfiguration, name="silly_config",
                      context=context)
    
