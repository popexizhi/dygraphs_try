# -*- coding:utf8
from ReportTempletX import * 
from ReportIfram import * 
import re,sys
class source_data():
    def __init__(self, fp, dir=None):
        f = open(fp)    
        com = f.readlines()
        f.close()
	self.dir = dir
	self.fkind = None
        self.init_data(com)

    
    def init_data(self, com):
        self.tabledata=None
        self.csv=[]
        self.title=None
        self.testtime=None
        self.des=None
	self.destabledata=None
	self.iframelist=None
        for i in com:
            i = re.sub("\n", "", i)
            x = i.split(":")    
            if len(x)<2: #字段过小不处理
                continue
            if "tabledata" == x[0]:
		if None == self.tabledata:
                	self.tabledata=[["name", "max", "min", "num", "avg", "stdev"]]
			self.fkind = "templet_data"
		
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
	    if "destabledata" == x[0]:
		# destabledata:fgw:(2)
		if None == self.destabledata :
			self.destabledata = []
			self.fkind = "output_data"
                self.destabledata.append([x[1], x[2]])
	    if "iframe_list" == x[0]:
		if None == self.iframelist:
			self.iframelist = []	
		if None != self.dir:
			self.iframelist.append([x[1], "%s/%s" % (self.dir ,x[1])])
		else:
			self.iframelist.append([x[1], x[1]])

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

    def getkind(self):
	return self.fkind

    def log(self):
        print "$"*100
        print "[title] %s" % str(self.title)
        print "[testtime] %s" % str(self.testtime)
        print "[des] %s" % str(self.des)
        print "[csv] %s" % str(self.csv)
        print "-"*100
	if None == self.tabledata :
	    pass
	else:
       	    for i in self.tabledata:
                print "[tabledata] %s" % str(i)
        
	if None == self.destabledata :
	    pass
	else:
	    for i in self.destabledata:
		print "[destabledata] %s" % str(i)
	if None == self.iframelist:
	    pass
	else:
	    for i in self.iframelist:
		print "[iframe_list] %s" % str(i)
        print "$"*100

	

class report():
    def get_iframe_html(self, source_data):
        self.log(source_data)
	if "templet_data" == source_data.getkind():
        	return templet_data(source_data)
	if "output_data" == source_data.getkind():
        	return output_data(source_data)
        
    def log(self, html_source):
        html_source.log()
        
if __name__=="__main__":
    try:
	dir = sys.argv[2]
    except IndexError:
	dir = None
    x= source_data(sys.argv[1], dir)
    x.log()
    y = report()
    print "http://192.168.1.216/test/provision_test/load_test/cluster/%s" % str(y.get_iframe_html(x))

