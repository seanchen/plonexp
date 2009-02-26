## Controller Script Python "psc_workplace_execute_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=svnurl=''
##title=validates the svn url

from Products.CMFPlone import PloneMessageFactory as _
plone_utils=context.plone_utils

if not svnurl:
    state.setError('svnurl', _(u'Please set SVN URL for making build.'), 'svnurl_required')

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'), 'error')
    return state.set(status='failure')
else:
    return state
