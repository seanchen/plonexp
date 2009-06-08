## Controller Python Script "object_actionone"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=My Testing Action on Objects
##
# Example code:
# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote

request = container.REQUEST
RESPONSE = request.RESPONSE
# Return a string identifying this script.
msg = "This is the %s '%s' " % (script.meta_type, script.getId())

if script.title:
    msg += "(%s)" % html_quote(script.title)

msg += "in %s" % container.absolute_url()

context.plone_utils.addPortalMessage(msg)

return state.set(status = 'success') 
