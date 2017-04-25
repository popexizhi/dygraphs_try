#-*-coding:utf8-*-
import re,time,datetime, sys
from datetime import timedelta
IOSTAT=["rrqm/s","wrqm/s","r/s","w/s","rkB/s","wkB/s","avgrq-sz","avgqu-sz","await","r_await","w_await","svctm","%util"]
MPSTAT=["usr","nice","sys","iowait","irq","soft","steal","guest","gnice","idle"]
class changefile():
    def __init__(self, fp, savedir, stat_kind="iostat"):
        self.fp = fp
        self.stat_kind = stat_kind
        if None == self.fp:
            self.log("no fp is testcase doing")
        else:
            self.com = self.getfplist()
            self.savedir = savedir
        

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
                print "list:\t--%s--" % (str(i))
                self.log(str_[i], islist=2)
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
    def transpose2csv(self, row_com):
        """
        转置按列顺序切割为多个csv文件
        eg:
            time, rrqm/s wrqm/s r/s w/s rkB/s wkB/s avgrq-sz avgqu-sz await r_await w_await svctm %util
            ['2017-04-24 14:08:31', 'xvda', '0.00', '0.00', '0.00', '6.00', '0.00', '24.00', '8.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['2017-04-24 14:08:31', 'dm-0', '0.00', '0.00', '0.00', '6.00', '0.00', '24.00', '8.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['2017-04-24 14:08:31', 'dm-1', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['2017-04-24 14:08:22', 'xvda', '0.00', '5.00', '0.00', '3.00', '0.00', '28.00', '18.67', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['2017-04-24 14:08:22', 'dm-0', '0.00', '0.00', '0.00', '7.00', '0.00', '28.00', '8.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            ['2017-04-24 14:08:22', 'dm-1', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
            转储为 csv files : rrqm/s wrqm/s r/s w/s rkB/s wkB/s avgrq-sz avgqu-sz await r_await w_await svctm %util
            每个文件中包含 time,xvda,dm-0,dm-1 列内容
        """
        line_row_com = row_com[0] 
        files_num = len(line_row_com) - 2 #time，iostat中的设备名称不在此范围
        assert files_num >0 #至少要有一个非时间戳数据

        if "iostat" == self.stat_kind:
            #iostat_row_name=["rrqm/s","wrqm/s","r/s","w/s","rkB/s","wkB/s","avgrq-sz","avgqu-sz","await","r_await","w_await","svctm","%util"]
            iostat_row_name=IOSTAT
        if "mpstat" == self.stat_kind:
            iostat_row_name=MPSTAT

        assert len(iostat_row_name) == files_num #iostat存储使用
        res_com = {} #存储中间结果集
        rescom = {} #存储返回结果集

        for i in iostat_row_name:
            res_com[i] = [] #初始化结果存储,以字典方式存储每个列的csv

        #获得新文件中的列名称列表,要求全部设备数据在首次时间戳中都出现
        time_lab = line_row_com[0] #第一个时间戳
        new_csv_row = ["time"]   
        for line_row_com in row_com: 
            #首行标题处理
            if line_row_com[0] == time_lab: #时间戳未变化时，是结果集中同一行数据
                new_csv_row.append(line_row_com[1]) #列名称要求为第二个字段名称，iostat显示的格式为列名称
            #数据处理
            index = 0 #列游标清零    
            for list_name_in_files_num in xrange(files_num):
                file_name = iostat_row_name[index]
                res_com[file_name].append([line_row_com[0], line_row_com[index+2]]) #time, 对应列的数据 
                index = index + 1
        for i in res_com:
            self.log("***********************************filename:%s" % i)
            self.log(res_com[i], islist=2)
       
        csvfiles=[]
        for file in res_com:
            res = self.secrowstonrows(res_com[file], new_csv_row)
            self.log("***********************************filename:%s" % file)
            self.log(res) 
        
            rescom[file] = res
            fp = "%s_%s.csv" % (self.stat_kind , file)
            csvfiles.append(self.savecsv(fp, new_csv_row, res))

        self.log("***********************************all")
        self.log(rescom, islist=1) 
        return csvfiles, rescom
        
    def savecsv(self, fp, rowname, comlist):
        """
            save rowname+comlist in fp
        """
        #首行标题
        com = rowname[0]
        for i in rowname[1:]:
            com = "%s,%s" % (com, str(i))
        #数据处理
        for line in comlist:
            com = "%s\n%s" % (com, str(line)) 
        fp = re.sub("/","_", fp)
        fp = "%s/%s" % (self.savedir, fp)
        f = open(fp, "w")
        f.write(com)
        f.close()
        return fp


    def secrowstonrows(self, comlist, new_csv_row):
        """ 
        change 两列数据 to 同时间戳数据多列同行显示，eg:参见Sp2CsvTest.py:test_secrowstonrows().__doc__
        comlist为要求处理的数据列表
        new_csv_row为新数据集的列标题

        """
        tmp_table = comlist
        res = []
        res_csv_line = len(tmp_table)/(len(new_csv_row)-1) #新标题中首个为time字段
        self.log("res_csv_line:%s" % str(res_csv_line))
        for line in xrange(res_csv_line):
            line = line * (len(new_csv_row) - 1)
            com = "%s" % tmp_table[line][0] #time标签
            self.log("line:%s;com:%s" % (str(line), str(com)) )
            #中间数据相同时间节点，转储时做同一行数据的处理
            for i_new_csv_row in xrange(len(new_csv_row) - 1):
                data = tmp_table[i_new_csv_row + line ][1]
                com = "%s,%s" % (com, str(data)) 
            self.log("[file_res]%s" % str(com))
            res.append(com)
        return res
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
        #4.转置按列顺序切割为多个csv文件
        self.transpose2csv(row_com)

if __name__=="__main__":
    x = changefile(sys.argv[1], sys.argv[2], sys.argv[3])
    x.doing()
