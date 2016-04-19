import scrapy
from scrapy.crawler                 import CrawlerProcess
from scrapy.utils.project           import get_project_settings
from proxy_list.spiders.free_proxy  import FreeProxySpider
from proxy_list.items               import ProxyItem
from random                         import randrange

from proxy_list import settings

arg_list = [ arg for arg in settings.__dict__ if not arg.startswith("__") ]
new_settings = { arg:settings.__dict__[arg] for arg in arg_list }

process = CrawlerProcess(new_settings)
process.crawl(FreeProxySpider)
process.start()


