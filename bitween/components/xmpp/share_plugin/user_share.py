from sleekxmpp.plugins.base import BasePlugin
from . import stanza
from . import UserSharesStanza, ShareItemStanza, ResourceStanza, AddressStanza
from sleekxmpp.xmlstream import register_stanza_plugin
import logging

from .. import Addresses
from .. import contact_shares

logger = logging.getLogger(__name__)


class UserShares(BasePlugin):
    """
    Share Plugin
    """

    name = 'shares'
    description = 'UserShares'
    dependencies = set(['xep_0163'])
    stanza = stanza

    def plugin_end(self):
        """


        :return:
        """
        self.xmpp['xep_0030'].del_feature(feature=UserShares.namespace)
        self.xmpp['xep_0163'].remove_interest(UserShares.namespace)
        pass

    def session_bind(self, jid):
        register_stanza_plugin(UserSharesStanza, ResourceStanza, iterable=True)
        register_stanza_plugin(ResourceStanza, ShareItemStanza, iterable=True)
        register_stanza_plugin(ResourceStanza, AddressStanza, iterable=True)
        self.xmpp['xep_0163'].register_pep('shares', UserSharesStanza)

    def publish_shares(self, handle_infos=None, addresses=None, options=None,
                       ifrom=None, block=True, callback=None, timeout=None):
        """
        publish current shares and addresses

        :param handle_infos:
        :param addresses:
        :param options:
        :param ifrom:
        :param block:
        :param callback:
        :param timeout:
        :return:
        """

        logger.error(addresses.ip_v4 + addresses.ip_v6)
        logger.error(addresses.ports + addresses.nat_ports)

        # write shares to contact_shares
        contact_shares.clear_addresses(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource)
        contact_shares.clear_shares(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource)

        for h in handle_infos:
            if h.get('hash', False):
                contact_shares.add_share_by_info(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource, h)
        # and add our addresses
        logger.info('addresses: %s' % (addresses.ip_v4 + addresses.ip_v6))
        for address in addresses.ip_v4 + addresses.ip_v6:
            for port in addresses.ports + addresses.nat_ports:
                contact_shares.add_address(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource, address, port)
        logger.info('publishing shares: %s' % contact_shares.get_user(self.xmpp.boundjid.bare))


        # now we need to iterate over all of our resources and shares to publish the new state
        shares_stanza = UserSharesStanza()
        logging.info('publishing %s handles' % len(handle_infos))

        for resource in contact_shares.get_user(self.xmpp.boundjid.bare).keys():
            if contact_shares.get_resource(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource)['shares'] != {}:
                logging.debug('adding resource %s' % resource)
                resource_stanza = shares_stanza.add_resource(resource)

                shares = contact_shares.get_resource(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource)['shares']
                for share in shares:
                    logging.debug('adding share %s to stanza' % shares[share]['name'])
                    resource_stanza.add_share(shares[share]['hash'], shares[share]['name'], shares[share]['size'])

                logging.info('adding addresses')
                # add ipv4 and v6 addresses
                address_list = \
                    contact_shares.get_ipv4_addresses(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource)
                address_list += \
                    contact_shares.get_ipv6_addresses(self.xmpp.boundjid.bare, self.xmpp.boundjid.resource)

                logging.debug('addresslist: %s ' % address_list)
                for address in address_list:
                    logging.info('adding address %s:%s' % (address[0], str(address[1])))
                    resource_stanza.add_address(address[0], str(address[1]))
                    logging.debug('yup, added')

        logging.debug('publishing...')
        return self.xmpp['xep_0163'].publish(shares_stanza,
                                             node=UserSharesStanza.namespace,
                                             ifrom=ifrom,
                                             block=block,
                                             callback=callback,
                                             timeout=timeout)

    def stop(self, ifrom=None, block=True, callback=None, timeout=None):
        """
        Clear existing user tune information to stop notifications.
        """
        addresses = Addresses()
        self.publish_shares(handle_infos=[], addresses=addresses)
