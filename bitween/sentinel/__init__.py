import logging
logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)

from ..models import own_addresses, Addresses

from .sentinel import Sentinel