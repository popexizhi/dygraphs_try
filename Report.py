# -*- coding:utf8
from ReportTempletX import * 
import re,sys
class source_data():
    def __init__(self, fp):
        f = open(fp)    
        com = f.readlines()
        f.close()
        self.init_data(com)
    
    def init_data(self, com):
        self.tabledata=[["name", "max", "min", "num", "avg", "stdev"]]
        self.csv=[]
        self.title=None
        self.testtime=None
        self.des=None
        for i in com:
            i = re.sub("\n", "", i)
            x = i.split(":")    
            if len(x)<2: #字段过小不处理
                continue
            if "tabledata" == x[0]:
                res = self.init_tabledata(x)
                self.tabledata.append(x[1:2]+res)
            if "csv" == x[0]:
                self.csv.append(x[1])
            if "title" == x[0]:
                self.title = str(x[1])
            if "testtime" == x[0]:
                self.testtime = str(x[1])
            if "des" == x[0]:
                self.des = str(x[1])
    def init_tabledata(self, data_list, id=-1):
        """
        data_list = ['tabledata', 'app_server_275734.log.txt_172.16.110.2_tcp_throughput_downlink.log', '(199.219, 0.379813, 569.0, 186.63922181546567, 11.23183313929444)\n']
        id 是被分割的字段,默认为最后一个
        """
        com = data_list[id]
        com = re.sub("\n|\(|\)", "", com)
        x = com.split(",")
        print str(x)
        return x

    def log(self):
        print "$"*100
        print "[title] %s" % str(self.title)
        print "[testtime] %s" % str(self.testtime)
        print "[des] %s" % str(self.des)
        print "[csv] %s" % str(self.csv)
        print "-"*100
        for i in self.tabledata:
            print "[tabledata] %s" % str(i)
        print "$"*100


class report():
    def get_iframe_html(self, source_data):
        self.log(source_data)
        return templet_data(source_data)
        
    def log(self, html_source):
        html_source.log()
        
if __name__=="__main__":
    x= source_data(sys.argv[1])
    #x.log()
    y = report()
    print y.get_iframe_html(x)

