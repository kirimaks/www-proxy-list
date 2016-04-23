import unittest
import os
import sys
import re

import_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(import_dir)

from get_proxy import GetProxy

def get_many_proxy(num_of_proxy, proxy_obj):
    buff = []
    for i in range(num_of_proxy):
        cur_proxy = proxy_obj.get_proxy()

        if not cur_proxy.startswith("http"):
            return False

        buff.append(cur_proxy)

    if not (len(buff) == num_of_proxy):
        return False

    return True

def check_proxy(proxy):
    reg_expr = "^https?\:\/\/\d+\.\d+\.\d+\.\d+\:\d{2,5}$"
    return re.search(reg_expr, proxy)

class BaseTest(unittest.TestCase):
    def __init__(self, *pargs, **kwargs):
        unittest.TestCase.__init__(self, *pargs, **kwargs)

    def setUp(self):
        self.pl = GetProxy()

    def test_T1(self):
        """Get one proxy"""
        buff = self.pl.get_proxy()
        self.assertTrue(buff.startswith("http"))

    def test_T2(self):
        """Get many proxy"""
        self.assertTrue(get_many_proxy(15, self.pl))

    def test_proxy(self):
        """Generate proxy and test output"""
        self.shortDescription()
        proxy = self.pl.get_proxy()
        self.assertTrue(check_proxy(proxy), "%s doesn't match" % proxy)
        
        
if __name__ == "__main__":
    # Create test suite.
    test_kit = unittest.TestSuite()

    # Add tests to suite.
    for i in ("test_T1", "test_T2"):
        test_kit.addTest(BaseTest(i))

    for i in range(100):
        test_kit.addTest(BaseTest("test_proxy"))

    # Run tests.
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(test_kit)
