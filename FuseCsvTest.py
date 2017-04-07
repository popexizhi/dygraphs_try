#-*-coding:utf8-*-
from FuseCsv import fuse_csv
import unittest
class fuse_csv_test(unittest.TestCase):
    def test_fuse_data(self):
        file1 = "testdata/a.csv"
        file2 = "testdata/b.csv"
        res = "testdata/res.csv"
        t = fuse_csv(file1, file2)
        testres = t.getres(is_tot=None)
        arp = t.openfile(res)
        self.assertEqual(t.openfile(testres), arp)

    def test_save_stafile(self):
        file1 = "testdata/a.csv"
        file2 = "testdata/b.csv"
        res = "testdata/res.csv"
        t = fuse_csv(file1, file2)
        t.save_stafile("test")

    def test_fuse_data_start_less(self):
        file1 = "testdata/a_less.csv"
        file2 = "testdata/b.csv"
        res = "testdata/res_a_less.csv"
        t = fuse_csv(file1, file2)
        testres = t.getres(is_tot=None)
        arp = t.openfile(res)
        print "test_fuse_data_start_less testres:%s" % str(testres)
        print "test_fuse_data_start_less arp:%s" % str(arp)
        self.assertEqual(t.openfile(testres), arp)

    def test_diff_time(self):
        """
        测试diff_time
        t1 = "0327/120313"
        t2 = "0327/130313"
        1.比较/前的日期年月 2.比较/后的时分秒
        相同返回0， t1比t2提前返回-1, t1比t2晚返回1 
        """
        x = fuse_csv()
        
        t1 = "0327/120313"
        self.assertEqual(x.diff_time(t1, t1), 0) #同时刻
        t1 = "0327/120313"
        t2 = "0327/130313"
        self.assertEqual(x.diff_time(t1, t2), -1)# 时间小
        t1 = "0327/140315"
        t2 = "0330/130313"
        self.assertEqual(x.diff_time(t1, t2), -1)# 日期小
        t1 = "0327/130317"
        t2 = "0327/130313"
        self.assertEqual(x.diff_time(t1, t2), 1)# 时间晚
        t1 = "1227/130317"
        t2 = "1203/130313"
        self.assertEqual(x.diff_time(t1, t2), 1)# 日期晚
    def test_static_avg_list(self):
        """
        test static_avg_list for row_id=1,2,3
        """
        x = fuse_csv()
        com = [\
        ["1", "1", "21", "31"],
        ["2", "2", "22", "32"],
        ["3", "3", "23", "33"]\
        ] 
        res1 = x.static_avg_list(com, row_id=1)
        self.assertEqual(res1, (3.0, 1.0, 3.0, 2.0, 2.0/2)) #1
        res2 = x.static_avg_list(com, row_id=2)
        self.assertEqual(res2, (23.0, 21.0, 3.0, 22.0, 2.0/2)) #2
        res3 = x.static_avg_list(com, row_id=3)
        self.assertEqual(res3,(33.0, 31.0, 3.0, 32.0, 2.0/2)) #1
    def get_com(self, fp):
        f = open (fp)
        com = f.readlines()
        f.close()

        return com
if __name__=="__main__":
    unittest.main()


    def get_com(self, fp):
        f = open (fp)
        com = f.readlines()
        f.close()

        return com
if __name__=="__main__":
    unittest.main()

