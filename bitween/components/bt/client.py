# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO

this file holds the class for the bittorrent client

"""

import logging
import os
from os.path import expanduser
import sqlite3
import time
import sys
from threading import Thread

import libtorrent as lt

from . import Subscriber
from ..models import contact_shares
from . import handles

from . import logger

from .. import config
from .helpers import utf8_encoded

conf = config.conf


class BitTorrentClient(Thread, Subscriber):
    """
    Backend for the TorrentSession
    """

    def __init__(self):
        Thread.__init__(self)
        Subscriber.__init__(self, autosubscribe=True)

        self.statdb = os.path.join(expanduser("~"), '.bitween.db')
        self.setup_db()

        self.session = lt.session()

        self.session.set_alert_mask(lt.alert.category_t.all_categories)
        logger.info('libtorrent %s' % lt.version)

        self.handles = handles

        """-----alert categories-----
        error_notification
        peer_notification
        port_mapping_notification
        storage_notification
        tracker_notification
        debug_notification
        status_notification
        progress_notification
        ip_block_notification
        performance_warning
        stats_notification
        dht_notification
        rss_notification
        all_categories
        """

        self.end = False

        self.setup_settings()

        if conf.get('bt', False):
            if conf['bt'].get('ports', False):
                ports = conf['bt'].get('ports')
                try:
                    self.session.listen_on(ports[0], ports[1])
                except Exception as e:
                    logger.error('could not set ports for BT: %s' % e)


        # self.session.start_dht()
        # self.session.start_lsd()
        if conf.get("enable_upnp", False):
            self.session.start_upnp()
        else:
            self.session.stop_upnp()
        if conf.get("enable_natpmp", False):
            self.session.start_natpmp()
        else:
            self.session.stop_natpmp()

        self.session.stop_dht()
        # self.session.stop_lsd()

        self.resume()  # load torrents from db

        self.name = 'bt'
        self.publish('bt_ready')

    def setup_settings(self):
        """
        called by the init method. sets up some sane settings.

        :return:
        """
        # settings
        # pesettings = lt.pe_settings()
        # pesettings.in_enc_policy = lt.enc_policy.forced
        # pesettings.out_enc_policy = lt.enc_policy.forced
        # pesettings.allowed_enc_level = lt.enc_level.rc4
        # self.session.set_pe_settings(pesettings)

        session_settings = lt.session_settings()

        # session_settings.announce_to_all_tiers = False  # announce_to_all_tiers also controls how multi tracker torrents are treated. When this is set to true, one tracker from each tier is announced to. This is the uTorrent behavior. This is false by default in order to comply with the multi-tracker specification.
        # session_settings.announce_to_all_trackers = False  # announce_to_all_trackers controls how multi tracker torrents are treated. If this is set to true, all trackers in the same tier are announced to in parallel. If all trackers in tier 0 fails, all trackers in tier 1 are announced as well. If it's set to false, the behavior is as defined by the multi tracker specification. It defaults to false, which is the same behavior previous versions of libtorrent has had as well.
        # session_settings.connection_speed = 100  # connection_speed is the number of connection attempts that are made per second. If a number < 0 is specified, it will default to 200 connections per second. If 0 is specified, it means don't make outgoing connections at all.
        # session_settings.ignore_limits_on_local_network = True  # ignore_limits_on_local_network, if set to true, upload, download and unchoke limits are ignored for peers on the local network.
        # session_settings.peer_connect_timeout = 2  # peer_connect_timeout the number of seconds to wait after a connection attempt is initiated to a peer until it is considered as having timed out. The default is 10 seconds. This setting is especially important in case the number of half-open connections are limited, since stale half-open connection may delay the connection of other peers considerably.
        # session_settings.rate_limit_ip_overhead = True  # If rate_limit_ip_overhead is set to true, the estimated TCP/IP overhead is drained from the rate limiters, to avoid exceeding the limits with the total traffic
        # session_settings.allow_multiple_connections_per_ip = True  # allow_multiple_connections_per_ip determines if connections from the same IP address as existing connections should be rejected or not. Multiple connections from the same IP address is not allowed by default, to prevent abusive behavior by peers. It may be useful to allow such connections in cases where simulations are run on the same machie, and all peers in a swarm has the same IP address
        # session_settings.request_timeout = 5
        # session_settings.torrent_connect_boost = 100  # torrent_connect_boost is the number of peers to try to connect to immediately when the first tracker response is received for a torrent. This is a boost to given to new torrents to accelerate them starting up. The normal connect scheduler is run once every second, this allows peers to be connected immediately instead of waiting for the session tick to trigger connections.

        self.session.set_settings(session_settings)

        # extensions
        # self.session.add_extension(
        #    lt.create_metadata_plugin)  # Allows peers to download the metadata (.torren files) from the swarm directly. Makes it possible to join a swarm with just a tracker and info-hash.
        # self.session.add_extension(lt.create_ut_metadata_plugin)  # same, utorrent compatible
        # self.session.add_extension(lt.create_ut_pex_plugin)  # Exchanges peers between clients.
        # self.session.add_extension(
        #    lt.create_smart_ban_plugin)  # A plugin that, with a small overhead, can ban peers that sends bad data with very high accuracy. Should eliminate most problems on poisoned torrents.

    def setup_db(self):
        """
        called by the init method.
        sets up the sqlite database if there is none.

        :return:
        """
        dbfile = self.statdb
        if not os.path.exists(dbfile):
            conn = sqlite3.connect(dbfile)
            c = conn.cursor()
            c.execute(
                "CREATE TABLE torrents (magnetlink VARCHAR PRIMARY KEY, torrent BLOB, status BLOB, save_path VARCHAR)")
            conn.commit()
            conn.close()

    def __del__(self):
        logger.info("torrentsession exits!")
        # exit(0)

    def on_exit(self):
        self.safe_shutdown()

    def safe_shutdown(self):
        """
        sets the end variable which tells the run method to jump out
        of the handling loop and trigger the save_handle for each handle.

        :return:
        """
        self.end = True

    def handle_queue(self):
        if self.has_messages():
            topic, args, kwargs = self.get_message()
            try:
                f = getattr(self, 'on_%s' % topic)
                f(*args, **kwargs)
            except Exception as e:
                logger.error('something went wrong when calling on_%s: %s' % (topic, e))

    def handle_alert(self, alert):
        #   http://www.libtorrent.org/reference-Alerts.html
        if (alert.what() == "save_resume_data_alert") \
                or (alert.what() == "save_resume_data_failed_alert"):
            handle = alert.handle

        elif alert.what() == "torrent_update_alert":
            self.publish('publish_shares')
        elif alert.what() == "state_update_alert":
            self.publish('publish_shares')
        elif alert.what() == "file_error_alert":
            logger.error("FILE ERROR: %s" % alert.error)
            self.session.remove_torrent(alert.handle)
            self.handles.remove(alert.handle)
            self.publish('publish_shares')
        elif (alert.what() == "stats_alert"):
            pass
        elif (alert.what() == "listen_failed_alert"):
            logger.error('failed to listen on interface %s: %s' % (alert.listen_interface(), alert.message()))
        # elif alert.what() == "external_ip_alert":  # todo
        #    ip = alert.external_address
        #    logger.info('got our ip: %s' % ip)
        #    self.publish('set_ip_address', ip)  # todo
        elif alert.what() == "portmap_alert":
            # http://www.rasterbar.com/products/libtorrent/manual.html#portmap-alert
            # This alert is generated when a NAT router was successfully found and a port was successfully mapped on it. On a NAT:ed network with a NAT-PMP capable router, this is typically generated once when mapping the TCP port and, if DHT is enabled, when the UDP port is mapped.
            self.publish('set_port', alert.external_port)
        elif alert.what() == "metadata_received_alert":
            # send shares when we have enough data to tell someone about it
            self.publish('publish_shares')
        elif alert.what() == "portmap_error_alert":
            logger.error('portmap error: %s' % alert.error)

        elif (alert.what() == "save_resume_data_alert"):
            handle = alert.handle
            self.save(handle, alert.resume_data)
            logger.debug("removing %s at %s" % (handle.name(), handle))
            self.session.remove_torrent(handle)
            # print(self.session.wait_for_alert(1000))
            self.handles.remove(handle)
        elif (alert.what() == "save_resume_data_failed_alert"):
            handle = alert.handle
            logger.debug("removing %s" % handle.name())
            self.session.remove_torrent(handle)
            self.handles.remove(handle)
        else:
            logging.debug('alert: %s - %s' % (alert.what(), alert.message()))

    def run(self):
        """
        the run method of the thread.

        this will process all the handles and messages in the input_queue.
        when safe_shutdown is called, it will trigger save_resume_data for every handle and wait for the alert
        with the resume_data.
        when every handle is deleted (after saving each resume_data), the session will be saved;
        were done and the thread will exit.
        """


        logger.debug("BT running")
        while not self.end:
            self.handle_queue()
            for alert in self.session.pop_alerts():
                self.handle_alert(alert)
            time.sleep(1)

        logger.debug("ending")
        # ending - save stuff
        # erase previous torrents first
        self.erase_all_torrents_from_db()

        # then trigger saving resume data
        for handle in self.handles:
            handle.save_resume_data(lt.save_resume_flags_t.flush_disk_cache)

        # set alert mast to get the right alerts
        self.session.set_alert_mask(lt.alert.category_t.storage_notification)

        # wait for everything to save and finish!
        while self.handles:
            # logger.debug(self.handles.list)
            for alert in self.session.pop_alerts():
                # logger.debug("- %s %s" % (alert.what(), alert.message()))
                self.handle_alert(alert)
        time.sleep(1)
        logger.debug("handles at return: %s" % self.handles)
        return

    def on_recheck_handles(self):
        for handle in self.handles:
            addr_tuples = contact_shares.hashes.get(str(handle.info_hash()), [])
            for addr_tuple in addr_tuples:
                try:
                    if addr_tuple not in [peer_info.ip for peer_info in handle.get_peer_info()]:
                        logger.info('connecting to %s' % addr_tuple[0])
                        handle.connect_peer((addr_tuple[0], int(addr_tuple[1])), 0)
                except Exception as e:
                    logger.error('recheck_handles: cant connect to %s:%s: %s' %
                                 (addr_tuple[0], addr_tuple[1], e))

    def on_add_hash(self, sha_hash, save_path):
        """
        add a hash to the torrent session
        used to download new stuff.

        after creation of the torrent all addresses that we have collected for the hash will be added

        :param sha_hash: hash of the torrent
        :type sha_hash: str
        :param save_path: path to save
        :type save_path: str
        :return:
        """
        mlink = 'magnet:?xt=urn:btih:%s' % sha_hash
        params = {
            'save_path': save_path,
            'duplicate_is_error': True
        }
        logger.debug('adding new handly by magnetlink')
        handle = lt.add_magnet_uri(self.session, utf8_encoded(mlink), params)
        self.handles.append(handle)

        logger.debug('adding peers to handle...')
        addr_tuples = contact_shares.hashes.get(sha_hash, [])
        if not addr_tuples:
            logger.error('no addresses for %s' % sha_hash)
            return None

        for addr_tuple in addr_tuples:
            logger.debug('adding peer to %s: %s:%s'
                         % (sha_hash, addr_tuple[0], addr_tuple[1]))
            try:
                handle.connect_peer((addr_tuple[0], int(addr_tuple[1])), 0)
            except Exception as e:
                logger.error('cant connect to %s:%s: %s' %
                             (addr_tuple[0], addr_tuple[1], e))

    '''
    def on_add_torrent(self, torrentfilepath, save_path):
        """
        creates a handle for a torrentfile and adds it to the session

        :param torrentfilepath: string with the path to the torrentfile
        :param save_path: string with the path to save
        :return:
        """
        logger.info("adding torrentfile")
        # info = lt.torrent_info(torrentfilepath)
        info = lt.torrent_info(lt.bdecode(open(torrentfilepath, 'rb').read()))
        self.add_torrent_by_info(info, save_path)
        self.publish('publish_shares')
    '''

    def _add_torrent_by_info(self, torrentinfo, save_path, resumedata=None):
        """
        needed to resume torrents by the saved resume_data

        also used by on_generate_torrent

        :param torrentinfo: the torrentinfo
        :param save_path: path to save
        :param resumedata: resume_data
        :return:
        """
        if not resumedata:
            logger.debug("no resume data!")
            handle = self.session.add_torrent(
                {
                    'ti': torrentinfo,
                    'save_path': save_path
                })
        else:
            logger.debug('resuming')
            handle = self.session.add_torrent(
                {
                    'ti': torrentinfo,
                    'save_path': save_path,
                    'resume_data': resumedata
                })

        self.handles.append(handle)
        self.publish('publish_shares')

    def on_generate_torrent(self, path):
        """
        generates a handle for a file or folder

        :param path: path to generate a handle for
        :type path: str
        :return:
        """
        logging.info('generating a new torrent for %s in %s' % (
            os.path.abspath(path), os.path.abspath(os.path.join(os.path.abspath(path), os.pardir))))

        fs = lt.file_storage()
        lt.add_files(fs, os.path.abspath(path))
        t = lt.create_torrent(fs)
        t.set_creator('bitween')  # %s' % lt.version)
        lt.set_piece_hashes(t,
                            os.path.abspath(os.path.join(
                                path,
                                os.pardir)))  # file and the folder it is in
        torrent = t.generate()
        logger.debug('generated')
        info = lt.torrent_info(torrent)
        self._add_torrent_by_info(info, save_path=os.path.abspath(os.path.join(
            path,
            os.pardir)))

    def on_del_torrent(self, hash):
        """
        delete a torrent from the current session.

        :param handle:
        :return: True, or False if not found
        """
        for handle in self.handles:
            if str(handle.info_hash()) == utf8_encoded(hash):
                self.session.remove_torrent(handle)
                self.handles.remove(handle)
                logger.info('removing handle for %s' % hash)
                self.publish('publish_shares')
                return True
                # else:
                #     print("%s != %s" % (handle.info_hash(), utf8_encoded(hash)))
                #     print("%s != %s" % (type(handle.info_hash()), type(utf8_encoded(hash))))
        return False

    def save(self, handle, resume_data):
        """
        called when the "save_resume_data_alert" is recieved while shutdown.
        saves handle with resume_data to database

        :param handle:
        :param resume_data:
        :return:
        """
        logger.debug('saving handle %s' % handle.name())
        save_path = handle.save_path()
        torrent = lt.create_torrent(handle.get_torrent_info())
        torfile = lt.bencode(torrent.generate())
        magnet = lt.make_magnet_uri(handle.get_torrent_info())
        status = lt.bencode(resume_data)

        db = sqlite3.connect(self.statdb)
        # create table torrents (magnetlink varchar(256), torrent blob, status blob);
        c = db.cursor()
        c.execute("INSERT OR REPLACE INTO torrents VALUES (?, ?, ?, ?)",
                  (magnet, sqlite3.Binary(torfile), sqlite3.Binary(status), save_path))
        db.commit()
        db.close()

    def resume(self):
        """
        reads the sessionsettings from db file and sets them,
        reads handles from db file and adds them to the session.

        :return:
        """
        # load state
        db = sqlite3.connect(self.statdb)
        c = db.cursor()

        # load last torrents
        erg = c.execute("SELECT * FROM torrents")
        for t in erg.fetchall():
            logger.info("importing %s" % t[0])
            entry = lt.bdecode(bytes(t[1]))
            fastresumedata = bytes(t[2])
            save_path = t[3]
            torrentinfo = lt.torrent_info(entry)
            self._add_torrent_by_info(torrentinfo, save_path=save_path, resumedata=fastresumedata)
        db.close()
        pass

    def erase_all_torrents_from_db(self):
        """
        removes all torrents from the session.
        called before the current torrents are going to be saved

        :return:
        """
        db = sqlite3.connect(self.statdb)
        c = db.cursor()
        c.execute("DELETE FROM torrents")
        db.commit()
        db.close()
