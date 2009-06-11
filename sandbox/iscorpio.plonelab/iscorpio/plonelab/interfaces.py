# interfaces.py

"""
"""

from zope.interface import Interface
from zope.interface import Attribute

class IPlonelabTool(Interface):
    """
    services and properties for iscorpio.plonelab.  it will save
    properties and provides some utility services.
    """

    id = Attribute('id', 'Must be set to "iscorpio_plonelab"')
