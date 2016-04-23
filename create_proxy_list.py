#!/usr/bin/evn python

"""
This module calls scrapy and stores it's
output (list of proxy servers) to database.
Possibly called by cron.
"""

from proxy_list.spiders.free_proxy  import FreeProxySpider
from proxy_list.items               import ProxyItem
from proxy_list                     import settings
from scrapy.utils.project           import get_project_settings
from scrapy.crawler                 import CrawlerProcess
from random                         import randrange
import scrapy


# Calculate settings.
arg_list = [arg for arg in settings.__dict__ if not arg.startswith("__")]
new_settings = {arg: settings.__dict__[arg] for arg in arg_list}

process = CrawlerProcess(new_settings)
process.crawl(FreeProxySpider)
process.start()
