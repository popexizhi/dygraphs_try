# -*- coding:utf8
from ReportTempletX import * 
import re,sys
class source_data():
    def __init__(self, fp):
        f = open(fp)    
        com = f.writelines()
        f.close()
        self.init_data(com)
    
    def init_data(self, com):
        self.tabledata=[]
        self.csv=[]
        for i in com:
            x = i.split(":")    
            if len(x)<2: #字段过小不处理
                continue
            if "tabledata" == x[0]:
                self.tabledata.append(x)
            if "csv" == x[0]:
                self.csv.append(x)
    

    def log(self):
        pass


class report():
    def get_iframe_html(self, source_data):
        self.log(source_data)

        
    def log(self, html_source):
        html_source.log()
        
if __name__=="__main__":
    x= source_data(sys.avgr[1])
