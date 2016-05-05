from sleekxmpp.plugins.base import register_plugin

from .share_item import ShareItem
from . import stanza
from .stanza import UserSharesStanza
from .user_share import UserShares

register_plugin(UserShares)