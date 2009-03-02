# testAtctType.py

""" we will do the basic unit test for the new content types based on
ATContentTypes.
"""

import unittest

from Products.ATContentTypes.tests.atcttestcase import ATCTTypeTestCase
from Products.ATContentTypes.tests.test_atfolder import TestSiteATFolder
from Products.ATContentTypes.tests.test_atdocument import TestSiteATDocument

from iscorpio.plonepm.content.PPMProject import PPMProject
from iscorpio.plonepm.content.PPMFuncSpec import PPMFuncSpec
from iscorpio.plonepm.content.PPMMetadata import PPMMetadata
from iscorpio.plonepm.content.PPMArtifact import PPMArtifact

from iscorpio.plonepm.tests.base import PlonepmTestCase

# test cases list
tests = []

class TestPPMProject(TestSiteATFolder):
    """ Testing basics about the AT Content Types within this product.
    """

    klass = PPMProject
    portal_type = "PPMProject"
    # the title in the types xml file.
    title = 'XP Project'
    meta_type = 'PPMProject'
    icon = 'XPProject_icon.gif'

tests.append(TestPPMProject)

class TestPPMFuncSpec(TestSiteATFolder):

    klass = PPMFuncSpec
    portal_type = "PPMFuncSpec"
    title = 'XP Function Spec'
    meta_type = "PPMFuncSpec"
    icon = 'xppm_fsd_icon.gif'

tests.append(TestPPMFuncSpec)

class TestPPMArtifact(TestSiteATFolder):

    klass = PPMArtifact
    portal_type = 'PPMArtifact'
    title = 'XP Artifact'
    meta_type = 'PPMArtifact'
    icon = 'xppm_artifact_icon.gif'

tests.append(TestPPMArtifact)

class TestPPMMetadata(ATCTTypeTestCase):

    klass = PPMMetadata
    portal_type = 'PPMMetadata'
    title = 'XP Metadata'
    meta_type = 'PPMMetadata'
    icon = 'xppm_metadata_icon.gif'

tests.append(TestPPMMetadata)

# making test suite.
def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    return suite
