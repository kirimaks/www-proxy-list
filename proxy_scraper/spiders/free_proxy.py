# -*- coding: utf-8 -*-
import scrapy
from .. import items
from scrapy.http import Request


class FreeProxySpider(scrapy.Spider):
    name = "free_proxy"
    allowed_domains = ["free-proxy-list.net", "http://hideme.ru"]

    start_urls = (
        'http://hideme.ru/proxy-list/',
        'http://hideme.ru/proxy-list/?start=64',
        'http://hideme.ru/proxy-list/?start=128',
        'http://free-proxy-list.net',
    )

    def __init__(self, *pargs, **kwargs):
        scrapy.Spider.__init__(self, *pargs, **kwargs)
        self.callbacks = {
            self.start_urls[0]: self.parser2,
            self.start_urls[1]: self.parser2,
            self.start_urls[2]: self.parser2,
            self.start_urls[3]: self.parser1,
        }

    def make_requests_from_url(self, url):
        return Request(url, callback=self.callbacks[url])

    def parser1(self, response):
        """ Parser for http://free-proxy-list.net """

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

    def parser2(self, response):
        """ Parser for http://hideme.ru/proxy-list/ """

        tbody = response.xpath("//tbody")
        trs = tbody.xpath("tr")

        for tr in trs:
            cur_proxy = items.ProxyItem()

            protocol = tr.xpath("td[5]/text()").extract()[0]
            protocol = protocol.strip().lower()
            if protocol in ("socks4", "socks5", "socks4, socks5"):
                continue
            elif protocol == "http, https":
                protocol = "https"
            cur_proxy['protocol'] = protocol
            cur_proxy['address'] = tr.xpath("td[1]/text()").extract()[0]
            cur_proxy['port'] = tr.xpath("td[2]/text()").extract()[0]
            buff = tr.xpath("td[3]/div/text()").extract()[0]
            cur_proxy['country'] = buff.strip()

            yield cur_proxy
