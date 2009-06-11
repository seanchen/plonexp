# tools.py

"""
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import SimpleItemWithProperties
from Products.CMFCore.utils import registerToolInterface

from interfaces import IPlonelabTool

class PlonelabTool(UniqueObject, SimpleItemWithProperties):
    """
    We implement it to just save some properties!
    """

    implements(IPlonelabTool)

    id = 'iscorpio_plonelab'
    meta_type = 'iScorpio Plonelab Tool'

    security = ClassSecurityInfo()

    _properties = (
        { 'id' : 'contact_email',
          'type' : 'string',
          'mode' : 'w',
          'label' : 'Your Contact Email'
          },

        { 'id' : 'favorite_color',
          'type' : 'string',
          'mode' : 'w',
          'label' : 'Your Favorite Color'
          },
        )

    contact_email = ''
    favorite_color = 'testing ...'

InitializeClass(PlonelabTool)
registerToolInterface('iscorpio_plonelab', IPlonelabTool)
