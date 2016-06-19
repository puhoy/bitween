Welcome to bitween's documentation!
===================================

Bitween is a more or less experimental XMPP/BitTorrent Client i develop as part of my bachelor thesis.

Right now its pretty basic and far from done.


things you will need
--------------------
on ubuntu
~~~~~~~~~

tested on python2,7, could work on python3

clone to where ever you like::

    git clone git@github.com:puhoy/bitween.git

install dependencies (virtualenv)::

    sudo apt-get install python-libtorrent
    virtualenv --system-site-packages env
    source env/bin/activate
    pip install ipgetter sleekxmpp flask flask-jsonrpc netifaces humanize

or install dependencies to system::

    sudo apt-get install python-libtorrent
    sudo pip install ipgetter sleekxmpp flask flask-jsonrpc netifaces humanize


configuring
-----------

copy the conf.json.dist to conf.json and fill in your xmpp credentials.
use as many accounts as you like. the save_path is the default save path to download to.


::

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


starting the daemon
===================

::

    python bitweend.py


this will start the daemon. you will have a web interface for the JSONRPC API on localhost:5000/api/browse

optional::

    -b '0.0.0.0'    # bind to something other than 127.0.0.1. might be useful if you want to use it on a server.
    -p 5000         # bind the API interface to another port


adding files to share::

    python bitweenc.py --add_file /path/to/file


get file hashes to download::

    python bitweenc.py --list

this will list all the files you have got via xmpp, so if you have not added an account before start, nothing will be listed here.


download files by hash::

    python bitweenc.py --add_hash some_sha1_hash




API Reference
-------------

.. toctree::
   :maxdepth: 2


   bitween


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

