import logging

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)
from .. import Subscriber

from ..models import handles
from ..models import contact_shares

from .client import BitTorrentClient

