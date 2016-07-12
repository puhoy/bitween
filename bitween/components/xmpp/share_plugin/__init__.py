from sleekxmpp.plugins.base import register_plugin

from .address_stanza import AddressStanza
from .share_item_stanza import ShareItemStanza
from . import stanza
from .stanza import UserSharesStanza
from .user_share import UserShares


register_plugin(UserShares)