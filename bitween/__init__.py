"""
this module loads the configuration and ensures that a default save path is available
"""

import json
import os

here = os.path.join(os.path.abspath(os.path.dirname(__file__)))

with open(os.path.join(here, '..', 'conf.json')) as f:
    conf = json.load(f)

# create default dir for storing data we leech
save_path = conf.get('save_path', 'share')
if not os.path.isdir(save_path):
    os.mkdir(save_path)
