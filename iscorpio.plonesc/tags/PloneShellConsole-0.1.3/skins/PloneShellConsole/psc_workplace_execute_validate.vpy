## Controller Script Python "psc_workplace_execute_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=exepurpose='', svnurl='', svnuser='', svnpassword=''
##title=validates the svn url

from Products.CMFPlone import PloneMessageFactory as _
plone_utils=context.plone_utils

if not exepurpose:
    state.setError('exepurpose', _(u'Please set the purpose for making build.'), 'exepurpose_required')

if not svnurl:
    state.setError('svnurl', _(u'Please set SVN URL for making build.'), 'svnurl_required')

if not svnuser:
    state.setError('svnuser', _(u'Please set SVN Username for making build.'), 'svnuser_required')

if not svnpassword:
    state.setError('svnpassword', _(u'Please set SVN Password for making build.'), 'svnpassword_required')

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'), 'error')
    return state.set(status='failure')
else:
    return state
