# __init__.py

from tools import PlonelabTool

def initialize(context):
    """
    Initializer called when used as a Zope 2 product.
    """

    # register tool.
    from Products.CMFCore.utils import ToolInit

    ToolInit('iScorpio Plonelab Tool',
             tools = (PlonelabTool,),
             icon = 'tool.gif'
             ).initialize(context)
