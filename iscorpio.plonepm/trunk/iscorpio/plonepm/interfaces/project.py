
# project.py

"""
all interfaces about project.
"""

from zope.interface import Interface

__author__ = "Sean Chen"
__email__ = 'chyxiang@gmail.com'
__docformat__ = 'plaintext'

# the project interface
class IPPMProject(Interface):
    """
    defines the interfaces for a project. empty for now.
    """
    pass

# end of class IPPMProject

# the story interface
class IPPMStory(Interface):
    """
    the interface for a story.
    """
    pass

# end of class IPPMStory

# the interation interface
class IPPMIteration(Interface):
    """
    the marker interface for a interation.
    """
    pass

# end of class IPPMIteration
