
# project.py

"""
all interfaces about project.
"""

from zope.interface import Interface

__author__ = "Sean Chen"
__email__ = 'chyxiang@gmail.com'
__docformat__ = 'plaintext'

class IPPMProject(Interface):
    """
    defines the interfaces for a project. empty for now.
    """
    pass

# end of class IPPMProject

class IPPMStory(Interface):
    """
    the interface for a story.
    """
    pass

# end of class IPPMStory
