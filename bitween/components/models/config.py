import os
import json
from . import logger


here = os.path.join(os.path.abspath(os.path.dirname(__file__)))

if os.path.isfile(os.path.join(here, '..', '..', 'conf.json')):
    with open(os.path.join(here, '..', '..', 'conf.json')) as f:
        conf = json.load(f)
else:
    logger.error('could not find conf.json')
    conf = {
        "xmpp_account": {},
        "save_path": "share",
        "enable_web_api": True,
        "enable_ipv4": True,
        "enable_ipv6": True,
        "enable_upnp": True,
        "enable_natpmp": True
    }

# create default dir for storing data we leech
save_path = conf.get('save_path', 'share')
if not os.path.isdir(save_path):
    os.mkdir(save_path)