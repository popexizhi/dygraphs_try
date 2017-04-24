#-*-coding:utf8-*-
import re,time,datetime, sys
from datetime import timedelta
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
     
    def gettime(self, comlist):
        """
        从首行数据中获得起始时间和间隔时间
        """
        assert len(comlist) > 1 #首行数据一定存在
        start_time = "%s %s" % (comlist[0][0], comlist[0][1])
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        space_time = int(comlist[1][0])
        self.log("start_time %s" % start_time)
        self.log("space_time %s" % space_time)
        return start_time, space_time

    def space_com(self, comlist, start_time, space_time):
        """
        分割时间轴下的数据片
        eg:
            iostat 原始数据为:
            ['time+1']
            ['xvda', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['dm-0', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['time+1']
            ['xvda', '0.00', '0.00', '0.00', '2.00', '0.00', '8.00', '8.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['time+1']

            分割后为:
            '2017-04-24 14:08:08':[
            ['xvda', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['dm-0', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ],
            '2017-04-24 14:08:09':[
            ['xvda', '0.00', '0.00', '0.00', '2.00', '0.00', '8.00', '8.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ]
            '2017-04-24 14:08:10':[]

        """
        com = {}
        timelab = "time+1"
        time = start_time
        
        for i in comlist:
            if timelab == i[0]:
                #时间分割标记位置,处理时间戳
                now_time = "%s" % str(time)
                com[now_time] = []
                time = time + timedelta(seconds=space_time) #时间标记按分割时间递增
                self.log("new time %s" % time)
            else:
                com[now_time].append(i)

        return com        
    def doing(self):
        """
        1.获得是起始时间和时间分割间隔
        2.切分时间段
        3.切分列数据
        
        """
        #1.获得是起始时间和时间分割间隔
        sta, spa = self.gettime(self.com)
        #2.切分时间段
        self.space_com(self.com[2:], sta, spa)

if __name__=="__main__":
    x = changefile(sys.argv[1])
    x.doing()
