.. image:: http://readthedocs.org/projects/bitween/badge/?version=develop
   :target: http://bitween.readthedocs.io/en/develop/?badge=develop
   :alt: Documentation Status

.. image:: https://travis-ci.org/puhoy/bitween.svg?branch=develop
   :target: https://travis-ci.org/puhoy/bitween
   :alt: Build Status


.. image:: https://coveralls.io/repos/github/puhoy/bitween/badge.svg?branch=develop
   :target: https://coveralls.io/github/puhoy/bitween?branch=develop
   :alt: Coverage Status


Welcome to bitween's documentation!
===================================

Bitween is a more or less experimental XMPP/BitTorrent Client i develop as part of my bachelor thesis.

Right now its pretty basic and far from done.


things you will need
--------------------
on ubuntu
~~~~~~~~~

tested on python2.7, could work on python3

clone to where ever you like::

    git clone git@github.com:puhoy/bitween.git

install dependencies (virtualenv)::

    sudo apt-get install python-libtorrent python-dev
    cd bitween
    virtualenv --system-site-packages -p /usr/bin/python2.7 env
    source env/bin/activate
    pip install -e .

or install dependencies to system::

    sudo apt-get install python-libtorrent python-dev
    sudo pip install -e .

configuring
-----------

copy the conf.json.dist to conf.json or ~/.bitween.conf and fill in your xmpp credentials.
the save_path is the default save path to download to.


.. code-block:: none

    {
      "xmpp_account": {
          "jid": "user@domain",
          "password": ""
      }

      "save_path": "share",
      "enable_ipv4": true,
      "enable_ipv6": false,
      "enable_upnp": true,
      "enable_natpmp": true
    }


starting the daemon
===================

::

    # (in the virtual env)
    bitweend


this will start the daemon. you will have a web interface for the JSONRPC API on localhost:5000/api/browse

optional::

    -b '0.0.0.0'    # bind to something other than 127.0.0.1. might be useful if you want to use it on a server.
    -p 5000         # bind the API interface to another port


adding files to share::

    bitweenc --add_path /path/to/file


get file hashes to download::

    bitweenc --list

this will list all the files you have got via xmpp, so if you have not added an account before start, nothing will be listed here.


download files by hash::

    bitweenc --add_hash some_sha1_hash
