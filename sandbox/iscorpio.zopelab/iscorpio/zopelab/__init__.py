# __init__.py

"""
The initialize method will seat here. This method will be invoked
when Zope server start up.
"""

from one import simple

# zope initialize method.
def initialize(context):
    """
    context will be passed from Zope server
    """

    context.registerClass(
        simple.SimpleProduct,
        constructors = (
            simple.manage_addSimpleProductForm,
            simple.manage_addSimpleProduct,
        ),
        visibility = None
    )
