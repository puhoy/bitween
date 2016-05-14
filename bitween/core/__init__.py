import json
import os

"""
load config & do (core-)global stuff
"""

with open('conf.json') as f:
    conf = json.load(f)

# create default dir for storing data we leech
save_path = conf.get('save_path', 'share')
if not os.path.isdir(save_path):
    os.mkdir(save_path)


"""
http://stackoverflow.com/questions/6319207/are-lists-thread-safe

lists seem to be thread safe, so this is the process-wide list of handles.
"""

