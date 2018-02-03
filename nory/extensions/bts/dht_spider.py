import logging

from maga import Maga


class Crawler(Maga):
    async def handle_get_peers(self, infohash, addr):
        logging.info(
            "Receive get peers message from DHT {}. Infohash: {}.".format(
                addr, infohash
            )
        )

    async def handle_announce_peer(self, infohash, addr, peer_addr):
        logging.info(
            "Receive announce peer message from DHT {}. Infohash: {}. Peer address:{}".format(
                addr, infohash, peer_addr
            )
        )



