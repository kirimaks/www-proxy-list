#!/usr/bin/evn python

"""
This module calls scrapy and stores it's
output (list of proxy servers) to database.
Possibly called by cron.
"""

from proxy_scraper.spiders.free_proxy import FreeProxySpider
from proxy_scraper import settings
from scrapy.crawler import CrawlerProcess


# Calculate settings.
arg_list = [arg for arg in settings.__dict__ if not arg.startswith("__")]
new_settings = {arg: settings.__dict__[arg] for arg in arg_list}

process = CrawlerProcess(new_settings)
process.crawl(FreeProxySpider)
process.start()
