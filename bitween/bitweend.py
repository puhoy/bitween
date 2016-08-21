import logging
from argparse import ArgumentParser

from bitween.components import config
from bitween.components.xmpp import XmppClient
from bitween.log import setup_logging

import os

import json
from os.path import expanduser

logger = logging.getLogger(__name__)

def start(api_host, api_port, conf):
    c = XmppClient(conf['xmpp_account']['jid'], conf['xmpp_account']['password'], api_host, api_port)
    c.connect()
    c.process()

def load_conf():

    home = expanduser("~")

    here = os.path.join(os.path.abspath(os.path.dirname(__file__)))

    conf = {}

    if os.path.isfile(os.path.join(here, '..', '..', 'conf.json')):
        logger.info('loading conf from %s', os.path.join(here, '..', '..', 'conf.json'))
        with open(os.path.join(here, '..', '..', 'conf.json')) as f:
            conf = json.load(f)

    elif os.path.isfile(os.path.join(home, '.bitween.json')):
        logger.info('loading conf from %s', os.path.join(home, '.bitween.json'))
        with open(os.path.join(home, '.bitween.json')) as f:
            conf = json.load(f)

    else:
        logger.error('could not find conf.json')
        print('no config file found!')
        print('you can find a sample config file in %s. (fill out and put it in ~/.bitween.json)' % os.path.abspath(
            os.path.join(here, '..', '..', 'conf.json.dist')))
        if not os.environ.get('BITWEEN_TESTING', "") == "True":
            exit(0)

    # create default dir for storing data we leech
    save_path = conf.get('save_path', 'share')
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    conf['save_path'] = save_path
    return conf

def main(args=None):
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("-b", "--bind", default='localhost')
    parser.add_argument("--debug", default=False, action='store_true')

    args = parser.parse_args()

    if args.debug:
        setup_logging(default_level=logging.DEBUG)
    else:
        setup_logging(default_level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('starting up')
    
    conf = load_conf()

    config.conf = conf
    config.save_path = conf['save_path']

    start(args.bind, args.port, conf)


if __name__ == "__main__":
    main()
