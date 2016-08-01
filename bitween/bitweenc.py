import json
import logging
import os
import random
from argparse import ArgumentParser

import humanize
import requests

from components.log import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

"""
POST /api
{
  "date": "Wed, 04 May 2016 11:00:06 GMT",
  "server": "Werkzeug/0.11.5 Python/2.7.6",
  "content-length": "90",
  "content-type": "application/json",
  "data": {
    "jsonrpc": "2.0",
    "method": "Api.exit",
    "params": [],
    "id": "e998df3f-523b-4533-915f-99bc2936f1bf"
  }
}
"""


class BitweenClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def post(self, method, params=None):
        if params is None:
            params = []
        data = {"jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": "%s" % random.randint(1000, 9999)}
        ret = requests.post("http://%s:%s/api" % (self.host, self.port), data=json.dumps(data))
        return ret

    def exit(self):
        method = "Api.exit"
        print(self.post(method))

    def list(self):
        hashes = {}
        method = "Api.get_all_torrents"
        contacts = self.post(method).json()['result']
        # print(contacts)

        for contact in contacts:
            for resource in contacts[contact]:
                for hash, val_dict in contacts[contact][resource]['shares'].iteritems():
                    c = hashes.get(hash, {'contacts': []}).get('contacts')
                    c.append('%s/%s' % (contact, resource))
                    hashes[hash] = {'name': val_dict['name'],
                                    'size': val_dict['size'],
                                    'contacts': c}

        # print(json.dumps(hashes, indent=2))
        for h, v in hashes.iteritems():
            print("%s - %s - %s \n-- %s" % (h, humanize.naturalsize(v['size']), v['name'], ', '.join(v['contacts'])))

    def add_hash(self, hash, dest=None):
        import os
        if not dest:
            dest = json.load(open('conf.json'))['save_path']
        method = "bt.add_torrent_by_hash"
        params = {
            "hash": hash,
            "save_path": os.path.abspath(dest)
        }
        print(self.post(method, params))

    def add_path(self, path):
        method = "bt.add_path"
        params = {
            "path": path
        }
        print(self.post(method, params))


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("-b", "--bind", default='localhost')
    parser.add_argument("--exit", default=False, action='store_true')
    parser.add_argument("--list", default=False, action='store_true')
    parser.add_argument("--add_hash")

    parser.add_argument("--dest")
    parser.add_argument("--add_path")
    parser.add_argument("--debug", default=False, action='store_true')

    args = parser.parse_args()

    bc = BitweenClient(args.bind, args.port)

    if args.exit:
        bc.exit()
    elif args.list:
        bc.list()
    elif args.add_hash:
        if not args.dest:
            bc.add_hash(args.add_hash)
        else:
            bc.add_hash(args.add_hash, args.dest)
    elif args.add_path:
        print('adding %s' % os.path.abspath(args.add_path))
        bc.add_path(args.add_path)


if __name__ == '__main__':
    main()
