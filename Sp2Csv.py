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
    def log(self, str_, islist=0):
        if 0 == islist:
            print "%s" % str(str_)
        if 1 == islist:
            #字典打印
            for i in str_:
                print "list:\t--%s--%s" % (str(i), str(str_[i]))
        if 2 == islist:
            #二维数据打印
            for i in str_ :
                print "%s" % str(i)

                
     
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
        
        self.log(com, islist=1) 
        return com        
    def row_split(self, com):
        """
        com = {} key时间戳,value为此时间中的获得内容
        eg: iostat-- input
            2017-04-24 14:08:22--[['xvda', '0.00', '5.00', '0.00', '3.00', '0.00', '28.00', '18.67', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'], ['dm-0', '0.00', '0.00', '0.00', '7.00', '0.00', '28.00', '8.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'], ['dm-1', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']]
            output
            ['2017-04-24 14:08:22', 'xvda', '0.00', '5.00', '0.00', '3.00', '0.00', '28.00', '18.67', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['2017-04-24 14:08:22', 'dm-0', '0.00', '0.00', '0.00', '7.00', '0.00', '28.00', '8.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['2017-04-24 14:08:22', 'dm-1', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']

        """
        reslist = [] 
        for key in com:
            for line in com[key]:
                reslist.append([key]+line[:])
        self.log(reslist, islist=2)
        self.log("[row_split]")
        return reslist

    def doing(self):
        """
        1.获得是起始时间和时间分割间隔
        2.切分时间段
        3.切分列数据
        4.转置按列顺序切割为多个csv文件
        
        """
        #1.获得是起始时间和时间分割间隔
        sta, spa = self.gettime(self.com)
        #2.切分时间段
        com = self.space_com(self.com[2:], sta, spa)
        #3.切分列数据
        row_com = self.row_split(com)

if __name__=="__main__":
    x = changefile(sys.argv[1])
    x.doing()
