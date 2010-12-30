
# utils.py

"""
Some handy facility script.
"""

import re

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# sourceforge.net revision number pattern, it is using subervision
SF_REVISION_PATTERN = r'(r([0-9]+))'
# github.com commit id pattern. git using SHA1 as unique id and the
# first 7 chars are good enough to make it unique.
GIT_COMMIT_PATTERN = r'(r([0-9a-f]{7,40}))'

# supported version control systems (VCS)
VCS_SF = 'sourceforge'
VCS_GITHUB = 'github'
VCS_TRAC = 'trac'

# the revision template for the revision number.
TEMPLATE_SF = "<a href='%s?view=rev&revision=%s'>%s</a>"
TEMPLATE_GITHUB = "<a href='%s/commit/%s'>%s</a>"
TEMPLATE_TRAC = "<a href='%s/changeset/%s'>%s</a>"

def revision2Link(description, linkBase):
    """
    convert the reversion number to web view changeset.
    """

    # check the link base to find out the source code repository
    # type: sourceforge, github, trac, etc.
    vcs_type = checkRepoType(linkBase)

    newDesc = description
    if vcs_type == VCS_SF:
        revisions = re.findall(SF_REVISION_PATTERN, description)
        template = TEMPLATE_SF

    elif vcs_type == VCS_GITHUB:
        revisions = re.findall(GIT_COMMIT_PATTERN, description)
        template = TEMPLATE_GITHUB

    elif vcs_type == VCS_TRAC:
        template = TEMPLATE_TRAC
        # trac support different types fo VCS, we will try git first
        # and then subversion.
        revisions = re.findall(GIT_COMMIT_PATTERN, description)
        if not revisions:
            # could not find pattern, it will return [], which
            # could be checked as false.
            # try the subversion pattern.
            revisions = re.findall(SF_REVISION_PATTERN, description)
    else:
        # NOT support VCS type.
        return newDesc

    for rNumber, number in revisions:

        link = template % (linkBase, number, rNumber)
        newDesc = newDesc.replace(rNumber, link)

    return newDesc

def checkRepoType(linkBase):
    """
    check the link base to decide what version control repository has
    been using.
    """

    if linkBase.find('sourceforge.net/') > -1:
        return VCS_SF

    elif linkBase.find('sf.net/') > -1:
        return VCS_SF

    elif linkBase.find('github.com/') > -1:
        return VCS_GITHUB

    elif linkBase.find('/trac/') > -1:
        return VCS_TRAC

    else:
        return None
