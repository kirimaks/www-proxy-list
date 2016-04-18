import scrapy
from scrapy.crawler                 import CrawlerProcess
from scrapy.utils.project           import get_project_settings
from proxy_list.spiders.free_proxy  import FreeProxySpider
from proxy_list.items               import ProxyItem
from random                         import randrange

class GetProxy:
    def __init__(self, debug=False, *pargs, **kwargs):
        self.results = []   
        process = CrawlerProcess(get_project_settings())
        process.crawl(FreeProxySpider, res = self.results )
        process.start()
        process.stop()

        if debug:
            print("Parsing done:")
            print("\tarray length is [{}] items.".format(len(self.results)))

    def get_random_proxy(self):
        return self.test_proxy()

    def test_proxy(self):
        return self.results[randrange(len(self.results))]

    def show_debug(self):
        print("Array length: {}".format(len(self.results)))

def init_proxy_list(*pargs, **kwargs):
    x = GetProxy(*pargs, **kwargs)
    return x

def get_proxy(obj):
    return obj.get_random_proxy()

def get_proxy_str(obj):
    proxy_obj = obj.get_random_proxy()
    return "{prot}://{addr}:{port}".format(prot = proxy_obj['protocol'], addr = proxy_obj['address'], port = proxy_obj['port'])


if __name__ == "__main__":
    plist = init_proxy_list(debug=True)

    for i in range(2):
        print(get_proxy(plist))
        
    for i in range(18):
        print(get_proxy_str(plist))
