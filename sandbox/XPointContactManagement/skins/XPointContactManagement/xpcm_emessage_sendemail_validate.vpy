## Controller Script Python "xpcm_emessage_sendemail_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=to=''
##title=validates the email adresses

from Products.CMFPlone import PloneMessageFactory as _
plone_utils=context.plone_utils

if not to:
    state.setError('to', _(u'Please set recipient email addresses.'), 'recipient_required')

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'), 'error')
    return state.set(status='failure')
else:
    return state
