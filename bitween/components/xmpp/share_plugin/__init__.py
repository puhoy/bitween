from sleekxmpp.plugins.base import register_plugin
from .share_item_stanza import ShareItemStanza
from .resource_stanza import ResourceStanza

from . import stanza
from .stanza import UserSharesStanza
from .user_share import UserShares


register_plugin(UserShares)