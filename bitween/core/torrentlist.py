import logging
from threading import Lock
from time import time

logger = logging.getLogger(__name__)

class Torrent:
    def __init__(self, size, sha_hash, name='', files=None):
        """

        :param size:
        :param hash:
        :param name:
        :param files:
        """
        if files is None:
            files = []
        self.hash = sha_hash
        self.names = [name]

        self.size = size
        self.files = files

        self.jids_lastseen = []
        # {"jid": "", "last_seen": ""}

    def add_name(self, name):
        self.names.append(name)

    def set_files(self, files):
        self.files = files


class TorrentList:
    def __init__(self):
        self.list = []
        self.lock = Lock()

    def add(self, jid, size, sha_hash, name='', files=None):
        with self.lock:
            found = False
            for t in self.list:
                if t.hash == sha_hash:
                    # we have this torrent, maybe we can add a filelist or name
                    if name:
                        if name not in t.names:
                            t.names.append(name)
                    if files:
                        t.files = files
                    t.jids_lastseen[jid] = time()
                    found = True
                    break

            if not found:
                t = Torrent(size, sha_hash, name='', files=None)
                self.list.append(t)
                
    def __iter__(self):
        with self.lock:
            for x in self.list:
                yield x

def search(term):
    pass