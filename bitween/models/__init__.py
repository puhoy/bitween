import logging

logger = logging.getLogger(__name__)
logger.debug('initializing %s' % __name__)

from .addresses import Addresses
from .contact_shares import ContactShares
from .own_shares import OwnShares


own_addresses = Addresses()
contact_shares = ContactShares()
own_shares = OwnShares([])
