
# testUtils.py

"""
unit test cases for utils in PlonePM
"""

from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite

from iscorpio.plonepm.utils import revision2Link

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestRevision2Link(TestCase):

    def testRevision2Link(self):

        # testing sourceforge
        description = 'this is a test revision r123'
        base_url = 'http://base.url.sf.net/projectname'

        result = "this is a test revision <a href='%s?view=rev&revision=%s'>%s</a>" % \
                 (base_url, '123', 'r123')

        formatedDesc = revision2Link(description, base_url)
        self.failUnless(formatedDesc == result)

        # testing github
        description = 'this is a test revision r123abced239017fea09372'
        base_url = 'http://github.com/username/projectname'

        result = "this is a test revision <a href='%s/commit/%s'>%s</a>" % \
                    (base_url, '123abced239017fea09372', 'r123abced239017fea09372')

        formatedDesc = revision2Link(description, base_url)
        self.failUnless(formatedDesc == result)

def test_suite():

    suite = TestSuite()
    suite.addTest(makeSuite(TestRevision2Link))

    return suite

    
