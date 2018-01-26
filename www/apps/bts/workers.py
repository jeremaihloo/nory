from infrastructures.apps import features
from apps.bts.dht_spider import Crawler
from infrastructures.apps.decorators import feature


@feature(features.__FEATURE_WORKER__, 'worker_dht_spider', 'worker_dht_spider')
async def worker_dht_spider():
    crawler = Crawler()
    # Set port to 0 will use a random available port
    crawler.run(port=0)