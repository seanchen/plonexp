
# interfaces.py

"""
marker intarfaces and schemas for tools
"""

from zope import schema
from zope.interface import Interface

class ISitesAdminConfig(Interface):
    """
    configuration properties for sites admin.  it will save
    properties and provides some utility services.
    """

    # using text area for products list
    productsNotToList = schema.Text(title=u"Enter Products Id Here, One Line for Each Product",
                                    required=True)
