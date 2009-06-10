# config.py

from zope.formlib import form
from zope.component import getUtility
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.i18nmessageid import MessageFactory

from OFS.SimpleItem import SimpleItem

from Products.Five.formlib import formbase

from interfaces import ISillyConfiguration

_ = MessageFactory('iscorpio.plonelab')

# the form class
class SillyConfigurationForm(formbase.EditFormBase):

    form_fields = form.Fields(ISillyConfiguration)

    label = _(u"A silly settings form")

# the utility class to do storage.
class SillyConfiguration(SimpleItem):

    implements(ISillyConfiguration)

    favorite_color = FieldProperty(ISillyConfiguration['favorite_color'])
    #contact_email = FieldProperty(ISillyConfiguration['contact_email'])

def form_adapter(context):

    return getUtility(ISillyConfiguration, name="silly_config",
                      context=context)
    
