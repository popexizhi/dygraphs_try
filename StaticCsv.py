#-*-coding:utf8-*-
import sys,re
from Static import static #数值分析使用
class static_csv():
    def __init__(self, fp1=None, fp2=None):
        self.com = []
	self.com1_sta = None
	self.com2_sta = None
        if None == fp1:
            pass 
        if None == fp2:
            self.com1 = self.openfile(fp1)
            self.log("self.com1 %s" % str(self.com1))
            self.com1_sta = self.static_avg_list(self.com1[1]) #fp1的数据分析结果
            self.fp1 = fp1.split("/")[-1].split(".csv")[0]
	else:
            self.com2 = self.openfile(fp2)
            self.log("self.com2 %s" % str(self.com2))
            self.fp2 = fp2.split("/")[-1].split(".csv")[0]
            self.com2_sta = self.static_avg_list(self.com2[1]) #fp2的数据分析结果
    def save_stafile(self, fp):
        """
        save self.com*_sta 到fp中:w
        """
        if  None != self.com1_sta:
        	com = "\ntabledata:%s:%s" % (self.fp1, str(self.com1_sta))
        if  None != self.com2_sta:
        	com = "%s\ntabledata:%s:%s" % (com, self.fp2, str(self.com2_sta))
        self.log(com)
        f = open(fp, "a") 
        f.write(com)
        f.close()
        return fp, com

    def name_use(self, str_):
        """
        str_="app_server_275734.log.txt_172.16.110.2"
        return app172.16.110.2
        str_="bgw.log.txt_192.168.1.114"
        return bgw192.168.1.114
        str_="app_server_275734.log.txt_172.16.110.2_down"
        return bgw192.168.1.114
        """
        line = str_.split("_")
        ip = re.findall("\d+.\d+.\d+.\d+", str_)[0]
        servername = line[0].split(".")[0]
        return "%s%s" % (servername, ip)

        
    def getres(self, fusefile=None, is_tot=1):
        #row_name fush
        row_name1 = self.name_use(self.fp1)
        row_name2 = self.name_use(self.fp2)
        new_name = [self.com1[0][0], "%s%s" % (row_name1, self.com1[0][1]), "%s%s" % (row_name2, self.com2[0][1])]
        self.log("row_name:%s" % str(new_name)) 
        #data fush
        len1 = len(self.com1[1]) 
        len2 = len(self.com2[1]) 
        j = 0
        i = 0
        while (i< len1 and j< len2):
            diff_res = self.diff_time(self.com1[1][i][0] , self.com2[1][j][0])
            self.log("diff_res %s" % str(diff_res))
            if 0 == diff_res: #同一个时间点
                self.com.append([self.com1[1][i][0], self.com1[1][i][1], self.com2[1][j][1]])
                j = j + 1
                i = i + 1
            if -1 == diff_res: #self.com1[1][i][0] 早,存self.com1
                old_com2 = 0 if 0 == j else self.com2[1][j-1][1] #如何前一个com2存在，补前一个时间点的内容，否则补0
                self.com.append([self.com1[1][i][0], self.com1[1][i][1], old_com2] )
                i = i + 1
            
            if 1 == diff_res: #self.com1[1][i][0] 晚,存self.com2
                old_com1 = 0 if 0 == i else self.com1[1][i-1][1] #如何前一个com1存在，补前一个时间点的内容，否则补0
                self.com.append([self.com2[1][j][0], old_com1, self.com2[1][j][1] ])
                j = j + 1
        if i < len1 : #self.com1有剩余数据
            for x in self.com1[1][i:]:
                self.com.append([x[0], x[1], '0'])
        if j < len2 : #self.com2有剩余数据
            for y in self.com2[1][j:]:
                self.com.append([y[0], '0', y[1]])
        
        fusefile = self.fusefile if None == fusefile else fusefile
        return self.savefile(new_name, self.com, fusefile, is_tot)
    def savefile(self, new_name, com, fp, is_tot):
        if None == is_tot:
            res = "%s,%s,%s" % (new_name[0], new_name[1], new_name[2])
            for i in com:
                time = "%s%s" % (i[0].split("/")[0], i[0].split("/")[1]) #time 为/分割的日期格式
                res="%s\n%s,%s,%s" % (res, str(time), str(i[1]), str(i[2]))
        if -1 == is_tot:
            #将tot写入time中
            res = "%s_total,%s,%s" % (new_name[0], new_name[1], new_name[2])
            for i in com:
                time = "%s%s_%s" % (i[0].split("/")[0], i[0].split("/")[1], str(float(i[1])+float(i[2])) ) #time 为/分割的日期格式
                res="%s\n%s,%s,%s" % (res, str(time), str(i[1]), str(i[2]))

        else:
            res = "%s,%s,%s,total" % (new_name[0], new_name[1], new_name[2])
            for i in com:
                time = "%s%s" % (i[0].split("/")[0], i[0].split("/")[1]) #time 为/分割的日期格式
                res="%s\n%s,%s,%s,%s" % (res, str(time), str(i[1]), str(i[2]), str(float(i[1])+float(i[2])))

        f = open(fp, "w")
        f.write(res)
        f.close()

        return fp

    def diff_time(self, t1 , t2):
        """
        t1 = "0327/120313"
        t2 = "0327/130313"
        1.比较/前的日期年月 2.比较/后的时分秒
        相同返回0， t1比t2提前返回-1 , t1比t2晚返回1
        """
        res = None
        t1 = t1.split("/")
        t2 = t2.split("/")
        assert 2 == len(t1)# 验证时间格式
        assert 2 == len(t2)# 验证时间格式
        if 0 == (int(t1[0]) - int(t2[0])):
            #继续比较
            
            if 0 == (int(t1[1]) - int(t2[1])):
                res = 0
            else:
                res = -1 if (int(t1[1]) - int(t2[1])) < 0 else 1
        else:
            return -1 if (int(t1[0]) - int(t2[0])) < 0 else 1

        return res
    
    def openfile(self, fp):
        f = open(fp)
        com = f.readlines()
        row_name = com[0].split("\n")[0].split(",")
        com = com[1:]
        com.sort() #排序
        #结构化
        com = self.struct_line(com) 
        f.close()
        return row_name, com

    def struct_line(self, com):
        struct_com = []
        for i in com:
            line = i.split("\n")[0] #去除换行符
            line = line.split(",") #分割csv格式
            struct_com.append(line)
            self.log(str(line))
        return struct_com
    def static_avg_list(self, com, row_id=-1):
        """
        com = [
        ['0327/120313', '0.142433', '0.142433']
        ['0327/120314', '62.5', '62.5']
        ['0327/120315', '125', '125']
        ['0327/120316', '187.5', '187.5']
        ['0327/120317', '250', '250']
        ['0327/120318', '0', '250']
        ['0327/120313', '0.142433', '0.142433']
        ['0327/120314', '62.5', '62.5']
        ]
        row_id为列号，默认为-1
        return float(Max), float(Min), float(num), float(avg), float(stdev)
        """
        #获得数值列表
        data_list = []
        for i in com:
            data_list.append(float(i[row_id]))
        self.log(data_list)
        #计算对应的分析数值
        sta = static()
        return sta.statistics_list(data_list)
    def log(self, str_):
        print "[fus_csv]-%s-" % str(str_)

if __name__=="__main__":
    t = static_csv(sys.argv[1])
    t.save_stafile(sys.argv[2])

