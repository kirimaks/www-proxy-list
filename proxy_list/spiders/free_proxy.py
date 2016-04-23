# -*- coding: utf-8 -*-
import scrapy
from .. import items


class FreeProxySpider(scrapy.Spider):
    name = "free_proxy"
    allowed_domains = ["free-proxy-list.net"]
    start_urls = (
        'http://free-proxy-list.net',
    )

    def parse(self, response):
        table = response.xpath("//table/tbody")
        trs = table.xpath("tr")

        for tr in trs:
            cur_proxy = items.ProxyItem()

            cur_proxy['address'] = tr.xpath("td[1]/text()").extract()[0]
            cur_proxy['port'] = tr.xpath("td[2]/text()").extract()[0]
            cur_proxy['country'] = tr.xpath("td[4]/text()").extract()[0]

            # get protocol "http/https"
            protocol = tr.xpath("td[7]/text()").extract()[0]
            cur_proxy['protocol'] = "https" if protocol == "yes" else "http"

            yield cur_proxy
