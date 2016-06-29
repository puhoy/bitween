import logging

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)

from ..models import own_shares
from ..models import own_addresses
from ..models import contact_shares

from .client import BitTorrentClient
