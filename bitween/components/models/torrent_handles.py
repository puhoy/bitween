from threading import Lock

from . import logger

class Handles:
    """
    holds a reference to the handles and some values for other threads

    this is managed by the bt thread
    """

    def __init__(self):
        logger.info('init handles')
        self.handles = []

    def __getitem__(self, key):
        return self.handles[key]

    def __setitem__(self, key, value):
        self.handles[key] = value

    def __delitem__(self, key):
        del self.handles[key]

    def __iter__(self):
        with Lock():
            for x in self.handles:
                yield x

    def __len__(self):
        return len(self.handles)

    def append(self, item):
        """
        append a handle to the handle list

        :param item:
        :return:
        """
        self.handles.append(item)

    def remove(self, item):
        """
        remove a handle from the handle list

        :param item:
        :return:
        """
        self.handles.remove(item)

    def get_shares(self):
        """
        get a list of own shares

        .. code-block:: json

            [{
                "files": [], # list of files
                "total_size": 0, # total size in bytes
                "name": "", # name of the torrent
                "hash": "", # sha hash
                "done": 0 # bytes done
            }]

        :return:
        """
        infos = []
        for handle in self.handles:
            try:
                info = handle.get_torrent_info()
                h = {}

                # h['handle'] = '%s' % handle
                h['files'] = []
                h['total_size'] = info.total_size()

                h['name'] = info.name()
                h['hash'] = u'%s' % handle.info_hash()

                h['done'] = handle.status().total_done

                try:
                    files = info.files()  # the filestore object
                except:
                    files = []

                for f in files:
                    h['files'].append(
                        {
                            'path': f.path,  # filename for file at index f
                            # 'size': files.file_size(f)
                        })
                infos.append(h)
            except Exception as e:
                logger.error('error while building torrent list: %s' % e)
        return infos
