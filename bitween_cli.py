from bitween.log import setup_logging
import logging
from datetime import datetime as dt

from argparse import ArgumentParser
import random
import json

setup_logging()
logger = logging.getLogger(__name__)

def _make_packet(method, payload=''):
    """POST /api
{
  "date": "Sun, 24 Apr 2016 15:38:09 GMT",
  "server": "Werkzeug/0.11.7 Python/2.7.9",
  "content-length": "90",
  "content-type": "application/json",
  "data": {
    "jsonrpc": "2.0",
    "method": "Api.exit",
    "params": [],
    "id": "38661dc2-b54d-493f-9c31-0efdd402d2ed"
  }
}"""
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": payload,
        "id": random.randint(1000, 9999)
    }
    return {
  "date": dt.now(),
  "server": "Werkzeug/0.11.7 Python/2.7.9",
  "content-length": json.dumps(data),
  "content-type": "application/json",
  "data": data
}

def _ask_api(method, payload=''):
    p = _make_packet(method, payload=payload)



def add_torrent(path):
    """
    adds a file to your shared files

    POST /api
{
  "date": "Sun, 24 Apr 2016 16:14:53 GMT",
  "server": "Werkzeug/0.11.7 Python/2.7.9",
  "content-length": "91",
  "content-type": "application/json",
  "data": {
    "jsonrpc": "2.0",
    "method": "bt.add_torrent",
    "params": {
      "file": "dfghfgh"
    },
    "id": "d7fb1910-76d0-4bc7-b8ed-64bec236e5cf"
  }
}

    :param path:
    :return:
    """
    pass

def search(term):
    pass

def list():
    method = "Api.get_all_torrents"
    return _ask_api(method)


def add_hash(hash):
    """
    download file with sha-1 hash "hash"

    :param hash: sha-1 hash do download
    :return:
    """
    method = "Api.get_all_torrents"
    return _ask_api(method)




if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("-s", "--server", default='localhost')
    parser.add_argument("--debug", default=False, action='store_true')


    args = parser.parse_args()


    if args.debug:
        setup_logging(default_level=logging.INFO)
    else:
        setup_logging(default_level=logging.DEBUG)

