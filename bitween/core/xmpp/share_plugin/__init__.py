from sleekxmpp.plugins.base import register_plugin

from . import stanza
from .stanza import UserSharesStanza
from .user_share import UserShares


register_plugin(UserShares)