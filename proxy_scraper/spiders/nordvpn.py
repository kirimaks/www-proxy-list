# -*- coding: utf-8 -*-
import scrapy
import json


class NordvpnSpider(scrapy.Spider):
    name = "nordvpn"
    start_urls = ['https://nordvpn.com/wp-admin/admin-ajax.php?searchParameters%5B0%5D%5Bname%5D=proxy-country&searchParameters%5B0%5D%5Bvalue%5D=&searchParameters%5B1%5D%5Bname%5D=proxy-ports&searchParameters%5B1%5D%5Bvalue%5D=&offset=0&limit=100000&action=getProxies']

    def parse(self, response):
        resp = json.loads(response.text)
        # {'country_code': 'VE', 'type': '', 'port': '8080', 'ip': '190.207.232.36', 'country': 'Venezuela'}

        # { "country" : "Canada", 
        #   "port" : "80", 
        #   "protocol" : "https", 
        #   "address" : "198.50.240.26", 
        #   "status" : "good" }
        proxies = [proxy for proxy in resp if proxy['type'] == 'HTTPS']

        for proxy in proxies:
            doc = {
                "country": proxy.get('country'),
                "port": proxy['port'],
                "protocol": proxy['type'].lower(),
                "address": proxy['ip']
            }
            yield doc
