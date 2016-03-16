from queue import Queue
from .main import create_xmpp_client

main_xmpp_queue = Queue()
xmpp_main_queue = Queue()

main_torrent_queue = Queue()
torrent_main_queue = Queue()


