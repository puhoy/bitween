# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sqlite3
import time
from threading import Thread
from types import FunctionType

import libtorrent as lt

from bitween.pubsub import PubSubscriber
from ..models import user_shares
from bitween.core.models import own_shares

logger = logging.getLogger(__name__)


class TorrentClient(Thread, PubSubscriber):
    """
    Backend for the TorrentSession
    """

    def __init__(self):
        Thread.__init__(self)
        PubSubscriber.__init__(self, autosubscribe=True)
        self.statdb = 'stat.db'
        self.settingname = 'defaultsetting'
        self.session = lt.session()
        self.state_str = ['queued', 'checking', 'downloading metadata', \
                          'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        self.session.set_alert_mask(lt.alert.category_t.all_categories)
        logger.info('libtorrent %s' % lt.version)

        self.handles = []

        self.session.listen_on(6881, 6891)

        # self.session.set_alert_mask(lt.alert.category_t.storage_notification)

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

        self.status = "stopped"

        self.setup_settings()
        self.setup_db()

        # logger.info('listening on port %s' % self.session.listen_port())
        # logging.info('listening on ssl_port %s' % self.session.ssl_listen_port())

        self.name = 'bt'
        self.publish('bt_ready')

    def setup_settings(self):
        """
        called by the init method. sets up some sane settings.

        :return:
        """
        # settings
        pesettings = lt.pe_settings()
        pesettings.in_enc_policy = lt.enc_policy.forced
        pesettings.out_enc_policy = lt.enc_policy.forced
        pesettings.allowed_enc_level = lt.enc_level.rc4
        self.session.set_pe_settings(pesettings)

        session_settings = lt.session_settings()

        session_settings.announce_to_all_tiers = True
        session_settings.announce_to_all_trackers = True
        session_settings.connection_speed = 100
        session_settings.peer_connect_timeout = 2
        session_settings.rate_limit_ip_overhead = True
        session_settings.request_timeout = 5
        session_settings.torrent_connect_boost = 100
        self.session.set_settings(session_settings)

        # extensions
        # self.session.add_extension(
        #    lt.create_metadata_plugin)  # Allows peers to download the metadata (.torren files) from the swarm directly. Makes it possible to join a swarm with just a tracker and info-hash.
        # self.session.add_extension(lt.create_ut_metadata_plugin)  # same, utorrent compatible
        # self.session.add_extension(lt.create_ut_pex_plugin)  # Exchanges peers between clients.
        self.session.add_extension(
            lt.create_smart_ban_plugin)  # A plugin that, with a small overhead, can ban peers that sends bad data with very high accuracy. Should eliminate most problems on poisoned torrents.

        # self.session.start_dht()
        # self.session.start_lsd()
        # self.session.start_upnp()
        # self.session.start_natpmp()
        self.session.stop_dht()
        self.session.stop_lsd()
        self.session.stop_natpmp()
        self.session.stop_upnp()

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
            c.execute("CREATE TABLE sessionstatus (settingname VARCHAR PRIMARY KEY, status BLOB)")
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
            '''
            elif d.get('pauseTorrent'):
                handle = d.get('pauseTorrent')
                status = handle.status()
                logger.info(status.paused)
                if not status.paused:
                    logger.debug('pausing')
                    handle.auto_managed(False)
                    handle.pause()
                else:
                    logger.debug('resume')
                    handle.auto_managed(True)
                    handle.resume()
            elif d.get('pause'):
                if self.session.is_paused():
                    self.pause(False)
                else:
                    self.pause(True)
            elif d.get('setprio'):
                # self.kju.put({'setprio': {'index': fileindex,'prio': prio,'handle': handle}})
                index = d.get('setprio').get('index')
                prio = d.get('setprio').get('prio')
                handle = d.get('setprio').get('handle')
                # TODO find out the possible priorities
                # the documentation doesnt seem to have that information...
                handle.file_priority(index, prio)
                logger.info('new file priorities: %s ' % handle.file_priorities())
            '''

    def pause(self, what):
        """ pauses or unpauses the session
        """
        if what:
            self.session.pause()
            self.status = 'paused'
        else:
            self.session.resume()
            self.status = 'running'

    # def setup_blocklist(self):
    #     """
    #     this will setup the blocklist in the session.
    #
    #     in case that the blocklistfile doesnt exist or is older
    #     than Blocklist().old_after_hours (5 hours by default) it will start a download which may take some time.
    #     """
    #     """TODO the parsing seems pretty ineffective. maybe i should do something."""
    #     blocklist = Blocklist()
    #
    #     self.statusbar.emit("%s - getting & parsing blocklist" % self.status)
    #     blocklist.setup_rules()
    #     rules = blocklist.get_rules()
    #
    #     self.statusbar.emit("%s - setting blocklist" % self.status)
    #     filter = lt.ip_filter()
    #     exceptions = 0
    #     for rule in rules:
    #         try:
    #             filter.add_rule(rule['from'], rule['to'], rule['block'])
    #         except:
    #             exceptions += 1
    #             if exceptions > 10:
    #                 return False
    #     self.session.set_ip_filter(filter)
    #     self.statusbar.emit("%s" % self.status)

    def run(self):
        """
        the run method of the thread.

        this will process all the handles and messages in the input_queue.
        when safe_shutdown is called, it will trigger save_resume_data for every handle and wait for the alert
        with the resume_data.
        when every handle is deleted (after saving each resume_data), the session will be saved;
        were done and the thread will exit.
        """
        # self.statusbar.emit(self.status)
        # self.output_queue.put({'status': self.status})
        # self.setup_blocklist()
        self.resume()

        self.status = "running"
        """
        print("settings:")
        for attr, value in self.session.get_settings().items():
            print("%s: %s" % (attr, value))
        """

        logger.info("lt läuft...")
        while not self.end:
            # neue events abarbeiten
            self.handle_queue()

            sessionstat = self.session.status()
            # logger.debug(sessionstat)

            # self.statusbar.emit("%.2f up, %.2f down @ %s peers - %s" % (
            #    sessionstat.upload_rate / 1024, sessionstat.download_rate / 1024, sessionstat.num_peers, self.status))

            # self.output_queue({'status': "%.2f up, %.2f down @ %s peers - %s" % (
            #    sessionstat.upload_rate / 1024, sessionstat.download_rate / 1024, sessionstat.num_peers, self.status)})

            for handle in self.handles:
                stat = handle.status()
                # logger.debug("%s - Progress: %s; Peers: %s; State: %s" %
                #             (handle.name(), stat.progress * 100, stat.num_peers, self.state_str[stat.state]))
                # self.torrent_updated.emit(handle, handle.status())

            for alert in self.session.pop_alerts():

                if (alert.what() == "save_resume_data_alert") \
                        or (alert.what() == "save_resume_data_failed_alert"):
                    handle = alert.handle
                elif alert.what() == "torrent_update_alert":
                    own_shares.rebuild(self.handles)
                elif alert.what() == "file_error_alert":
                    logger.info("%s" % alert.error)
                    self.session.remove_torrent(handle)
                    self.handles.remove(handle)
                    own_shares.rebuild(self.handles)
                elif (alert.what() == "stats_alert"):
                    pass
                elif alert.what() == "external_ip_alert":  # todo
                    ip = alert.external_address
                    logger.info('got our ip: %s' % ip)
                    self.publish('set_ip_address', ip)  # todo
                else:
                    logging.debug('alert: %s - %s' % (alert.what(), alert.message()))
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
                if (alert.what() == "save_resume_data_alert"):
                    handle = alert.handle
                    self.save(handle, alert.resume_data)
                    logger.debug("removing %s at %s" % (handle.name(), handle))
                    self.session.remove_torrent(handle)
                    # print(self.session.wait_for_alert(1000))
                    self.handles.remove(handle)
                    own_shares.rebuild(self.handles)
                elif (alert.what() == "save_resume_data_failed_alert"):
                    handle = alert.handle
                    logger.debug("removing %s" % handle.name())
                    self.session.remove_torrent(handle)
                    self.handles.remove(handle)
                    own_shares.rebuild(self.handles)
                elif (alert.what() == "stats_alert"):
                    pass
                else:
                    logger.info('got %s: %s' % (alert.what(), alert.message()))

        self.save_state()
        time.sleep(1)
        logger.debug("handles at return: %s" % self.handles)
        return

    def on_add_peer(self, infohash, peer_address, peer_port):
        """
        add a peer to an existing torrent which is identified by its magnetlink

        :param magnetlink:
        :param peer_address:
        :param peer_port:
        :return:
        """

        logger.debug('trying to add peer')
        # info = handle.torrent_file()
        # info.name()
        handle = False

        for h in self.handles:
            if infohash == '%s' % h.info_hash():
                logger.debug('hash found')
                handle = h
            else:
                logger.debug("%s is not %s" % (infohash, h.info_hash()))

        if handle:
            logger.info('adding peer %s to handle %s' % (peer_address, handle.name()))
            handle.connect_peer((peer_address, peer_port), 0)
            return True
        else:
            return False

    def on_add_hash(self, hash, save_path):
        mlink = 'magnet:?xt=urn:btih:%s' % hash
        params = {
            'save_path': save_path,
            'duplicate_is_error': True
        }
        link = mlink
        handle = lt.add_magnet_uri(self.session, link, params)
        self.handles.append(handle)
        own_shares.rebuild(self.handles)

        for ip in user_shares.hashes[hash]['ip_v4']:
            handle.connect_peer((ip, 6881), 0)

        self.publish('new_handle')


    def on_add_magnetlink(self, magnetlink, save_path):
        """
        creates a handle for a magnetlink and adds it to the session

        :param magnetlink: string with the magnetlink
        :param save_path: string with the path to save
        :return:
        """
        logger.info("adding mlink %s" % magnetlink)
        # handle = lt.add_magnet_uri(self.session, magnetlink, {'save_path': save_path})
        params = {
            'save_path': save_path,
            'duplicate_is_error': True
        }

        link = magnetlink
        handle = lt.add_magnet_uri(self.session, link, params)
        # params = lt.parse_magnet_uri(magnetlink)
        # logger.debug(params)

        # {'storage_mode': libtorrent.storage_mode_t.storage_mode_sparse,
        # 'source_feed_url': '',
        # 'name': 'Release.key',
        # 'trackers': [],
        # 'url': '',
        # 'ti': None,
        # 'info_hash': <libtorrent.sha1_hash object at 0x7f050ff2dad0>,
        # 'flags': 2147484272,
        # 'save_path': '',
        # 'dht_nodes': [],
        # 'uuid': ''}

        # params['info_hash'] = str(params['info_hash'])
        # logging.debug('hash as bytes: %s' % params['info_hash'])
        # handle = self.session.add_torrent(params)

        # logger.debug('added handle-hash %s' % handle.info_hash())
        # info = handle.torrent_file()
        # logger.debug('added handle-hash %s' % info.info_hash())

        self.handles.append(handle)
        own_shares.rebuild(self.handles)
        self.publish('new_handle')
        # self.torrent_added.emit(handle)

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
        self.on_add_torrent_by_info(info, save_path)
        self.publish('new_handle')

    def on_add_torrent_by_info(self, torrentinfo, save_path, resumedata=None):
        """
        needed to resume torrents by the saved resume_data

        :param torrentinfo: the torrentinfo
        :param save_path: path to save
        :param resumedata: resume_data
        :return:
        """
        if not resumedata:
            logger.debug("no resume data!")
            handle = self.session.add_torrent({'ti': torrentinfo, 'save_path': save_path})
        else:
            logger.debug('resuming')
            handle = self.session.add_torrent({'ti': torrentinfo, 'save_path': save_path, 'resume_data': resumedata})

        self.handles.append(handle)
        own_shares.rebuild(self.handles)
        self.publish('new_handle')
        # self.torrent_added.emit(handle)

    def on_generate_torrent(self, folder):
        '''
        generates a handle for a file or folder
        '''
        logging.info('generating a new torrent for %s in %s' % (
            os.path.abspath(folder), os.path.abspath(os.path.join(os.path.abspath(folder), os.pardir))))

        # shared_folder = 'shared'
        # for root, dirs, files in os.walk(shared_folder):
        #    for file in files:

        fs = lt.file_storage()
        lt.add_files(fs, os.path.abspath(folder))
        t = lt.create_torrent(fs)
        t.set_creator('bitween')  # %s' % lt.version)
        lt.set_piece_hashes(t,
                            os.path.abspath(os.path.join(
                                folder,
                                os.pardir)))  # file and the folder it is in
        logger.debug('...')
        torrent = t.generate()
        logger.debug('generated')
        info = lt.torrent_info(torrent)
        self.on_add_torrent_by_info(info, save_path=os.path.abspath(os.path.join(
            folder,
            os.pardir)))

    def on_del_torrent(self, handle):
        """saves the resume data for torrent
        when done, save_resume_data_alert will be thrown, then its safe to really delete the torrent
        """
        handle.save_resume_data(lt.save_resume_flags_t.flush_disk_cache)  # creates save_resume_data_alert
        # self.torrent_deleted.emit(handle)

    def save(self, handle, resume_data):
        """
        called when the "save_resume_data_alert" is recieved while ending.
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

    def save_state(self):
        """
        saves the session settings to db

        :return:
        """
        # create table sessionstatus (status blob)
        logger.debug('saving state')
        entry = self.session.save_state()
        encentry = lt.bencode(entry)
        db = sqlite3.connect(self.statdb)
        # create table torrents (magnetlink varchar(256), torrent blob, status blob);
        c = db.cursor()
        c.execute("INSERT OR REPLACE INTO sessionstatus VALUES (?, ?)", (self.settingname, sqlite3.Binary(encentry)))
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
        # erg = c.execute("SELECT * FROM sessionstatus")
        # f = erg.fetchone()
        # if f:
        #    encsettings = f[1]
        #    settings = lt.bdecode(bytes(encsettings))
        #    self.session.load_state(settings)
        #    logger.info("loaded settings: %s" % settings)

        # load last torrents
        erg = c.execute("SELECT * FROM torrents")
        for t in erg.fetchall():
            logger.info("importing %s" % t[0])
            entry = lt.bdecode(bytes(t[1]))
            fastresumedata = bytes(t[2])
            save_path = t[3]
            torrentinfo = lt.torrent_info(entry)
            self.on_add_torrent_by_info(torrentinfo, save_path=save_path, resumedata=fastresumedata)
        db.close()
        pass

    def erase_all_torrents_from_db(self):
        """
        removes all torrents from the session.
        done before the program quits to flush the db for the current torrents

        :return:
        """
        db = sqlite3.connect(self.statdb)
        c = db.cursor()
        c.execute("DELETE FROM torrents")
        db.commit()
        db.close()
