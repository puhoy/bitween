import logging

from ..models import contact_shares
from ..models import own_shares
from ..models import own_addresses

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)

from client import XmppClient
