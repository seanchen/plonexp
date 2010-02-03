# sillytest.py

from zope.component import getUtility

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from interfaces import ISillyConfiguration

class SillyTest(BrowserView):

    def __call__(self):

        context = aq_inner(self.context)
        conf = getUtility(ISillyConfiguration,
                          name='silly_config', context=context)

        labtool = getToolByName(context, "iscorpio_plonelab")

        props = getToolByName(context, 'portal_properties').plonelab_properties

        return 'utility: %s<br/> Tool: %s, %s<br/> Props: %s' % \
               (conf.favorite_color,
                labtool.contact_email, labtool.favorite_color,
                props.getProperty('favorite_color'))
