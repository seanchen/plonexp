# sillytest.py

from zope.component import getUtility

from Acquisition import aq_inner
from Products.Five import BrowserView

from interfaces import ISillyConfiguration

class SillyTest(BrowserView):

    def __call__(self):

        context = aq_inner(self.context)
        conf = getUtility(ISillyConfiguration,
                          name='silly_config', context=context)
        return conf.favorite_color

        
