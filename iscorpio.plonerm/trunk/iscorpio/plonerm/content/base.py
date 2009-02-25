
# base.py

__doc__ = """ We define the base class/content type in this package."""
__author__ = 'iscorpio@users.sourceforge.net'
__docformat__ = 'plaintext'

import logging
import transaction

# the base class
class PRMBaseContent:
    """ the base class for Plone Resource Management content type.
    """

    # The prefix for auto generated object id.  Each content can give it's
    # own prefix.
    prm_id_prefix = "prm"

    log = logging.getLogger("PloneResourceManagement PRMBaseContent")

    # override renameAfterCreation to generate the unique id for
    # contact. This method is defined in Archetypes.BaseObject.py.
    def _renameAfterCreation(self, check_auto_id=False):

        # Can't rename without a subtransaction commit when using
        # portal_factory!
        transaction.savepoint(optimistic=True)
        newId = str(self.getNextUniqueId())
        self.log.debug('the next value for prm sequence: %s',
                       newId)
        self.setId(self.prm_id_prefix + newId)
