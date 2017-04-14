import scrapy
from scrapy.crawler import CrawlerProcess
from proxy_scraper.spiders.free_proxy import FreeProxySpider
from proxy_scraper.spiders.nordvpn import NordvpnSpider
import proxy_scraper.settings

settings = dict()
for arg in [arg for arg in dir(proxy_scraper.settings) if not arg.startswith("__")]:
    settings[arg] = proxy_scraper.settings.__dict__[arg]


process = CrawlerProcess(settings)
process.crawl(FreeProxySpider)
process.crawl(NordvpnSpider)
process.start()
