import json
import logging
import os
import random
from argparse import ArgumentParser

import humanize
import requests

from bitween.log import setup_logging
from os.path import expanduser

setup_logging()
logger = logging.getLogger(__name__)


class BitweenClient:
    def __init__(self, host, port):
        """
        client class to access the bitweenc jsonrpc api

        basically this is a wrapper around a requests.post method

        :param host: bitweend host
        :param port: bitweend port
        """
        self.host = host
        self.port = port

    def post(self, method, params=None):
        """
        post data to run methods

        example calls looks like:

        .. code-block:: json

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


        :param method:
        :param params:
        :return:
        """

        if params is None:
            params = []
        data = {"jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": "%s" % random.randint(1000, 9999)}
        ret = requests.post("http://%s:%s/api" % (self.host, self.port), data=json.dumps(data))
        return ret

    def exit(self):
        """
        trigger exit of bitweend

        :return:
        """
        method = "Api.exit"
        print(self.post(method))

    def list(self):
        """
        list collected shares and their sources

        :return:
        """
        hashes = {}
        method = "xmpp.get_shares"
        res = self.post(method).json()
        # print(res)
        contacts = res['shares']

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
        """
        add a hash to download

        :param hash: sha1 hash of the torrent
        :param dest:
        :return:
        """
        import os
        if not dest:
            dest = conf['save_path']
        method = "bt.add_torrent_by_hash"
        params = {
            "hash": hash,
            "save_path": os.path.abspath(dest)
        }
        print(self.post(method, params))

    def add_path(self, path):
        """
        add a new torrent by path

        can be a file or a folder

        :param path:
        :return:
        """
        method = "bt.add_path"
        params = {
            "path": path
        }
        print(self.post(method, params))


def load_conf():
    """
    load a configuration file
    searches a json file at /path/to/bitween/conf.json and, if not found, at ~/.bitween.json

    :return:
    """
    home = expanduser("~")

    here = os.path.join(os.path.abspath(os.path.dirname(__file__)))

    conf = {}

    if os.path.isfile(os.path.join(here, 'conf.json')):
        logger.info('loading conf from %s', os.path.join(here, '..', '..', 'conf.json'))
        with open(os.path.join(here, 'conf.json')) as f:
            conf = json.load(f)

    elif os.path.isfile(os.path.join(home, '.bitween.json')):
        logger.info('loading conf from %s', os.path.join(home, '.bitween.json'))
        with open(os.path.join(home, '.bitween.json')) as f:
            conf = json.load(f)

    else:
        logger.error('could not find conf.json')
        print('no config file found!')
        print('you can find a sample config file in %s. (fill out and put it in ~/.bitween.json)' % os.path.abspath(
            os.path.join(here, 'conf.json.dist')))
        if not os.environ.get('BITWEEN_TESTING', "") == "True":
            exit(0)

    # create default dir for storing data we leech
    save_path = conf.get('save_path', 'share')
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    conf['save_path'] = save_path
    return conf


conf = load_conf()


def main(args=None):
    """
    main function for the client

    :param args:
    :return:
    """
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
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
