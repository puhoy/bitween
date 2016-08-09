import logging

from .. import contact_shares
from .. import handles
from .. import Addresses

from .. import publish

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)

from .client import XmppClient
