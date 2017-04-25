#-*-coding:utf8-*-
import unittest
from Sp2Csv import changefile
class changefile_test(unittest.TestCase):
    def test_transpose2csv(self):
        """
        test transpose2csv

        """
        x = changefile("testdata/192.168.1.113__iostat_tmp", "testdata")
        x.doing()
    def test_secrowstonrows(self):
        """
        change 
        [
        ['2017-04-24 14:08:08', '188.04']
        ['2017-04-24 14:08:08', '185.10']
        ['2017-04-24 14:08:08', '2.92']
        ['2017-04-24 14:08:09', '0.00']
        ['2017-04-24 14:08:09', '0.00']
        ['2017-04-24 14:08:09', '0.00']
        ['2017-04-24 14:08:24', '0.00']
        ['2017-04-24 14:08:24', '0.00'] 
        ['2017-04-24 14:08:24', '0.00'] ]
        to
        [
        ['2017-04-24 14:08:08,188.04,185.10,2.92']
        ['2017-04-24 14:08:09,0.00,0.00,0.00']
        ['2017-04-24 14:08:24,0.00,0.00,0.00']]
        """
        pass

        testlist=[
        ['2017-04-24 14:08:08', '188.04'],
        ['2017-04-24 14:08:08', '185.10'],
        ['2017-04-24 14:08:08', '2.92'],
        ['2017-04-24 14:08:09', '0.00'],
        ['2017-04-24 14:08:09', '0.00'],
        ['2017-04-24 14:08:09', '0.00'],
        ['2017-04-24 14:08:24', '0.00'],
        ['2017-04-24 14:08:24', '0.00'],
        ['2017-04-24 14:08:24', '0.00']]

        prelist=[
        '2017-04-24 14:08:08,188.04,185.10,2.92',
        '2017-04-24 14:08:09,0.00,0.00,0.00',
        '2017-04-24 14:08:24,0.00,0.00,0.00']
        x = changefile(None, None)
        realist = x.secrowstonrows(testlist, ["time", "x", "y", "z"])
        self.assertEqual(realist, prelist)
if __name__=="__main__":
    unittest.main()
