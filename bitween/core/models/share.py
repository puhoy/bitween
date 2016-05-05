import time

class Shares:
    def __init__(self):
        self.shares = {}

    def add_share(self, hash):
        if hash not in self.shares:
            self.shares[hash] = Share(hash)
        return self.shares[hash]

    def get(self, hash):
        if hash not in self.shares:
            return None
        return self.shares[hash]


class Share:
    def __init__(self, sha_hash):
        """
        :param size:
        :param hash:
        """

        self.hash = sha_hash
        self.size = 0

        self.names = set([])
        self.files = []

        self.seen = {}  # user: {"resource": time.time()}
        self.addresses = set([])

    def add_name(self, name):
        self.names.add(name)

    def set_files(self, files):
        self.files = files

    def seen(self, user, resource, timestamp=time.time()):
        user = self.seen.get(user, {})
        if not user:
            self.seen[user] = {}
        resource = user.get(resource, {})
        if not resource:
            self.seen[user][resource] = {}
        self.seen[user][resource] = timestamp

    @property
    def as_dict(self):
        d = {"hash": self.hash,
             "names": self.names,
             "size": self.size,
             "files": self.files}
        return d

