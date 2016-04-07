from threading import Lock

import logging
logger = logging.getLogger(__name__)

from libtorrent import make_magnet_uri

class HandleList:
    """
    holds a reference to the handles and some values for other threads
    """

    def __init__(self, handles):
        self.list = []
        self.lock = Lock()
        self.rebuild(handles)

    def rebuild(self, handles):
        self.list = []
        for handle in handles:
            self.add(handle)

    def add(self, handle):
        logger.debug('added file %s', handle.name())
        with self.lock:
            info = handle.torrent_file()
            h = {
                'handle': '%s' % handle,
                'files': [],
                'total_size': info.total_size(),
                'name': info.name(),
                'hash': info.info_hash(),
                'mlink': make_magnet_uri(info)
            }
            files = info.files()  # the filestore object
            for f in files:
                h['files'].append(
                    {
                        'path': f.path,  # filename for file at index f
                        #'size': files.file_size(f)
                    })
            logger.info('new files: %s' % h)
            self.list.append(h)

    def get(self, handle):
        with self.lock:
            for h in self.list:
                if h['handle'] is handle:
                    return h

    def remove(self, handle):
        logger.debug('removing handle')
        with self.lock:
            for h in self.list:
                if h['handle'] is '%s' % handle:
                    del h
                    return
                else:
                    logger.debug('%s is not %s' % (h['handle'], '%s' % handle))
            logger.debug('handle not found!')

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __delitem__(self, key):
        del self.list[key]

    def __iter__(self):
        with self.lock:
            for x in self.list:
                yield x
