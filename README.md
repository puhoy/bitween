# bitween

a somewhat experimental xmpp/bittorrent client


## things you will need
### on ubuntu

this should work from python 2.7 to 3.5 (so feel free to use pip3 / python3-libtorrent)

    sudo apt-get install python-libtorrent
    sudo pip install ipgetter sleekxmpp flask flask-jsonrpc netifaces humanize


## configuring

copy the conf.json.dist to conf.json and fill in your xmpp credentials.
use as many accounts as you like. the save_path is the default save path to download to.

        {
          "xmpp_accounts": [
            {
              "jid": "user@domain/resource",
              "password": "SuperSafePassword"
            }
          ],
          "save_path": "share"
        }



## starting the daemon

    python bitweend.py

this will start the daemon. you will have a web interface for the JSONRPC API on localhost:5000/api/browse

optional:

    -b '0.0.0.0'    # bind to something other than 127.0.0.1. might be useful if you want to use it on a server.
    -p 5000         # bind the API interface to another port


## adding files to share

    python term.py --add_file /path/to/file


## get file hashes to download

    python term.py --list

this will list all the files you have got via xmpp, so if you have not added an account before start, nothing will be listed here.


## download files by hash

    python term.py --add_hash some_sha1_hash

