import json
import os

from bitween.core.handlelist import HandleList

with open('conf.json') as f:
    conf = json.load(f)

if not os.path.isdir(conf['save_path']):
    os.mkdir(conf['save_path'])

"""
http://stackoverflow.com/questions/6319207/are-lists-thread-safe

lists seem to be thread safe, so this is the process-wide list of handles.
"""
handlelist = HandleList([])

