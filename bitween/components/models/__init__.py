import logging

logger = logging.getLogger(__name__)
logger.debug('initializing %s' % __name__)

from .contact_shares import ContactShares
from .torrent_handles import Handles
from . import config
from .addresses import Addresses

contact_shares = ContactShares()
handles = Handles()