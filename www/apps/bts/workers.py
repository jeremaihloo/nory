import events
from app_cores import app_fn
from apps.bts.dht_spider import Crawler


@app_fn(events.__EVENT_WORKER__, 'worker_dht_spider', 'worker_dht_spider')
async def worker_dht_spider():
    crawler = Crawler()
    # Set port to 0 will use a random available port
    crawler.run(port=0)