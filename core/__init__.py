import json
from core.bt.handlelist import HandleList

with open('conf.json') as f:
    conf = json.load(f)


"""
http://stackoverflow.com/questions/6319207/are-lists-thread-safe

lists seem to be thread safe, so this is the process-wide list of handles.
"""
handlelist = HandleList()

