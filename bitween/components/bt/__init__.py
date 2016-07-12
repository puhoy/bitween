import logging

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)
from .. import PubSubscriber

from ..models import handles
from ..models import contact_shares

from .client import BitTorrentClient

