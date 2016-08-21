import logging

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)

from .client import XmppClient
