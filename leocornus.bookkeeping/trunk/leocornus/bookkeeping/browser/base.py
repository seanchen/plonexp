
# base.py

"""
The base view class for all browser views in bookkeeping.
"""

import locale
from datetime import datetime

from Acquisition import aq_inner
from DateTime import DateTime

from Products.Five.browser import BrowserView

from leocornus.bookkeeping.util.catalog import getYearQuery

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class BaseView(BrowserView):
    """
    providing some utilities for browser view.
    """

    def monetary(self, number, place=2):
        """
        format the given number to monetary format
        """

        # set to locale to en_CA for monetary.
        locale.setlocale(locale.LC_MONETARY, 'en_CA.UTF-8')
        return locale.format('%.*f', (place, number), True)
