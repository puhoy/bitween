import os
import json
from . import logger

from os.path import expanduser
home = expanduser("~")


here = os.path.join(os.path.abspath(os.path.dirname(__file__)))

if os.path.isfile(os.path.join(here, '..', '..', 'conf.json')):
    with open(os.path.join(here, '..', '..', 'conf.json')) as f:
        conf = json.load(f)

elif os.path.isfile(os.path.join(home, '.bitween.json')):
    with open(os.path.join(home, '.bitween.json')) as f:
        conf = json.load(f)

else:
    logger.error('could not find conf.json')
    print('no config file found!')
    print('you can find a sample config file in %s. (fill out and put it in ~/.bitween.json)' % os.path.abspath(os.path.join(here, '..', '..', 'conf.json.dist')))
    exit(0)



# create default dir for storing data we leech
save_path = conf.get('save_path', 'share')
if not os.path.isdir(save_path):
    os.mkdir(save_path)