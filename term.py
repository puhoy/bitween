from bitween.log import setup_logging
import logging
import requests
import random
import json
from argparse import ArgumentParser

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
port = 0
host = ''
def post(method, params=None):
    if params is None:
        params = []
    data = {"jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": "%s" % random.randint(1000, 9999)}
    ret = requests.post("http://%s:%s/api" % (host, port), data=json.dumps(data))
    return ret

def exit():
    method = "Api.exit"
    print(post(method))


def list():

    import humanize
    hashes = {}
    method = "Api.get_all_torrents"
    contacts = post(method).json()['result']
    #print(contacts)

    for contact in contacts:
        for resource in contacts[contact]:
            for hash, val_dict in contacts[contact][resource]['shares'].iteritems():
                c = hashes.get(hash, {'contacts': []}).get('contacts')
                c.append('%s/%s' % (contact, resource))
                hashes[hash] = {'name': val_dict['name'],
                                'size': val_dict['size'],
                                'contacts': c}

    #print(json.dumps(hashes, indent=2))
    for h, v in hashes.iteritems():
        print("%s - %s - %s \n-- %s" % (h, humanize.naturalsize(v['size']), v['name'], ', '.join(v['contacts'])))

def add(hash, dest=None):
    if not dest:
        dest = json.load(open('conf.json'))['save_path']
    method = "bt.add_torrent_by_hash",
    params = {
      "hash": hash,
      "save_path": dest
    }
    print(post(method, params))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("-b", "--bind", default='localhost')
    parser.add_argument("--exit", default=False, action='store_true')
    parser.add_argument("--list", default=False, action='store_true')
    parser.add_argument("--debug", default=False, action='store_true')

    args = parser.parse_args()

    host = args.bind
    port = args.port

    if args.exit:
        exit()
    elif args.list:
        list()


