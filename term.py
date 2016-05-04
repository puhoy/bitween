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

def exit():
    data = {"jsonrpc": "2.0",
        "method": "Api.exit",
        "params": [],
        "id": "%s" % random.randint(1000, 9999)}
    post(data)

def post(data):
    ret = requests.post("http://%s:%s/api" % (host, port), data=json.dumps(data))
    print(ret.content)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("-b", "--bind", default='localhost')
    parser.add_argument("--exit", default=False, action='store_true')
    parser.add_argument("--debug", default=False, action='store_true')

    args = parser.parse_args()

    host = args.bind
    port = args.port

    if args.exit:
        exit()
