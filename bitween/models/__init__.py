import logging

logger = logging.getLogger(__name__)
logger.debug('initializing %s' % __name__)

from .contact_shares import ContactShares
from .own_shares import OwnShares
from . import config

contact_shares = ContactShares()
own_shares = OwnShares([])