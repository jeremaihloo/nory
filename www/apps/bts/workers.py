from infrastructures import events
from infrastructures.apps.coros import feature
from apps.bts.dht_spider import Crawler


@feature(events.__FEATURE_WORKER__, 'worker_dht_spider', 'worker_dht_spider')
async def worker_dht_spider():
    crawler = Crawler()
    # Set port to 0 will use a random available port
    crawler.run(port=0)