from threading import Lock


class HandleList:
    """
    holds a reference to the handles and some values for other threads
    """

    def __init__(self, handles: list):
        self.list = []
        self.lock = Lock()
        self.rebuild(handles)

    def rebuild(self, handles):
        self.list = []
        for handle in handles:
            self.add(handle)

    def add(self, handle):
        with self.lock:
            h = {
                    'handle': handle,  # functions from handle should not be called outside of the bt thread.
                    'files': [],
                    'total_size': handle.total_size(),
                    'name': handle.name()
                }
            files = handle.files()  # the filestore object
            for f in range(0, files.num_files()):
                h['files'].append(
                    {
                        'name': files.file_name(f),  # filename for file at index f
                        'size': files.file_size(f)
                    })
            self.list.append(h)

    def get(self, handle):
        with self.lock:
            for h in self.list:
                if h['handle'] is handle:
                    return h

    def remove(self, handle):
        with self.lock:
            for h in self.list:
                if h['handle'] is handle:
                    self.list.remove(h)
                    return

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __delitem__(self, key):
        del self.list[key]

    def __iter__(self):
        for x in self.list:
            yield x

