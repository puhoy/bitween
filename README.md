[![Documentation Status](https://readthedocs.org/projects/bitween/badge/?version=latest)](http://bitween.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/puhoy/bitween.svg?branch=develop)](https://travis-ci.org/puhoy/bitween)
[![Coverage Status](https://coveralls.io/repos/github/puhoy/bitween/badge.svg?branch=develop)](https://coveralls.io/github/puhoy/bitween?branch=develop)

# bitween

a somewhat experimental xmpp/bittorrent client


## things you will need
### on ubuntu

tested on python2,7, could work on python3

clone to where ever you like::

    git clone https://github.com/puhoy/bitween.git

install dependencies (virtualenv)::

    cd bitween
    sudo apt-get install python-libtorrent python-dev
    virtualenv --system-site-packages -p /usr/bin/python2.7 env
    source env/bin/activate
    pip install -r requirements.txt

or install dependencies to system::

    sudo apt-get install python-libtorrent python-dev
    sudo pip install -r requirements.txt


## configuring

copy the conf.json.dist to conf.json and fill in your xmpp credentials.
use as many accounts as you like. the save_path is the default save path to download to.

    {
      "xmpp_accounts": [
        {
          "jid": "user@domain",
          "password": ""
        }
      ],
      "save_path": "share",
      "enable_ipv4": true,
      "enable_ipv6": true,
      "enable_upnp": true,
      "enable_natpmp": true
    }



## starting the daemon

    python bitweend.py

this will start the daemon. you will have a web interface for the JSONRPC API on localhost:5000/api/browse

optional:

    -b '0.0.0.0'    # bind to something other than 127.0.0.1. might be useful if you want to use it on a server.
    -p 5000         # bind the API interface to another port


## adding files to share

    python bitweenc.py --add_file /path/to/file


## get file hashes to download

    python bitweenc.py --list

this will list all the files you have got via xmpp, so if you have not added an account before start, nothing will be listed here.


## download files by hash

    python bitweenc.py --add_hash some_sha1_hash

