# __init__.py

"""
The initialize method will seat here. This method will be invoked
when Zope server start up.
"""

from one import simple
from dove import nest
from dove import factory

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# zope initialize method.
def initialize(context):
    """
    context will be passed from Zope server
    """

    # retister the SimpleProduct
    context.registerClass(
        simple.SimpleProduct,
        constructors = (
            simple.manage_addSimpleProductForm,
            simple.manage_addSimpleProduct,
        )
    )

    # register the CMFDove
    context.registerClass(
        nest.CMFDove,
        constructors = (
            factory.manage_addDoveForm,
            factory.manage_addDove,
        )
    )
