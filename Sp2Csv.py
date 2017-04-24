#-*-coding:utf8-*-
import re,time,datetime, sys
class changefile():
    def __init__(self, fp):
        self.fp = fp
        self.com = self.getfplist()
        

    def getfplist(self):
        f = open(self.fp)
        com = []
        for i in f.readlines():
            i = re.sub("\n", "", i)
            line = i.split(",")
            self.log(line)
            com.append(line) 
        f.close()
        return com
    def log(self, str_):
        print "%s" % str(str_)

if __name__=="__main__":
    x = changefile(sys.argv[1])
