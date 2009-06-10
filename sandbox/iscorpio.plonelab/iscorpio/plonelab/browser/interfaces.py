# interfaces.py

from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('iscorpio.plonelab')

class ISillyConfiguration(Interface):
    """This interface defines the configlet.
    """

    favorite_color = schema.TextLine(title=_(u"Enter your favorite color"),
                                     required=True) 
