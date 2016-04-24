import unittest
import os
import sys
import re
import sqlite3

import_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(import_dir)

from get_proxy import GetProxy

db_name = "data.db"

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

def check_if_database_is_empty():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT count(*) FROM proxy_list")
    out = cursor.fetchone()
    if out == (0,):
        return False    # If no records in database, test error.

    return True

def check_unique_addresses():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute("select address, port, count(*) FROM proxy_list GROUP BY address, port HAVING count(*) > 1")
    out = cursor.fetchall()
    if len(out) > 1:
        print("%d not unique addresses" % len(out))
        return False

    return True


class BaseTest(unittest.TestCase):
    def __init__(self, *pargs, **kwargs):
        unittest.TestCase.__init__(self, *pargs, **kwargs)

    def setUp(self):
        self.pl = GetProxy()

    def test_T1(self):
        """Check if database is empty"""
        self.assertTrue(check_if_database_is_empty(), "Empty database!")

    def test_T2(self):
        """Get one proxy"""
        buff = self.pl.get_proxy()
        self.assertTrue(buff.startswith("http"))

    def test_T3(self):
        """Get many proxy"""
        self.assertTrue(get_many_proxy(15, self.pl))

    def test_T4(self):
        """Testing if database contains only unique proxy addresses"""
        self.assertTrue(check_unique_addresses(), "Not all addresses are unique.")

    def test_proxy(self):
        """Generate proxy and test output"""
        self.shortDescription()
        proxy = self.pl.get_proxy()
        self.assertTrue(check_proxy(proxy), "%s doesn't match" % proxy)


if __name__ == "__main__":
    # Create test suite.
    test_kit = unittest.TestSuite()

    # Add tests to suite.
    test_list = ("test_T1", "test_T2", "test_T3", "test_T4")
    for i in test_list:
        test_kit.addTest(BaseTest(i))

    # Get n proxies and test.
    for i in range(50):
        test_kit.addTest(BaseTest("test_proxy"))

    # Run tests.
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(test_kit)
