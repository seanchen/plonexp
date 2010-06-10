
# base.py

__doc__ = """ We define the base class/content type in this package for
xpoint contact management."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging
import transaction

# the base class
class XPCMBase:
    """ the base class for XPoint Contact Management content type.
    """

    # The prefix for auto generated object id.  Each content can give it's
    # own prefix.
    xpcm_id_prefix = "xpcm"

    log = logging.getLogger("XPointContactManagement XPCMBase")

    # override renameAfterCreation to generate the unique id for
    # contact. This method is defined in Archetypes.BaseObject.py.
    def _renameAfterCreation(self, check_auto_id=False):

        # Can't rename without a subtransaction commit when using
        # portal_factory!
        transaction.savepoint(optimistic=True)
        newId = str(self.getNextUniqueId())
        self.log.info('the next value for contact sequence: %s',
                      newId)
        self.setId(self.xpcm_id_prefix + newId)
