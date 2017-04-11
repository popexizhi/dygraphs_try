# -*- coding:utf8 -*-
import datetime, time
from ProcessDa import ProcessDa
import random
import sys, copy
from Static import *
DEFLOG = 0

class ana_rtt():
    def __init__(self):
        self.processt = ProcessDa()
        self.static = static()

    def doing(self, fp, sta, end, save_dir=None, is_change_to_second=1):
        """ 
        1.open file
        2.处理数据
        3.出x,y数据
        """
        #1
        datas = self.processt.file2matrix(fp)
        self.log(datas)
        if type(-1) == type(datas):
            return -1, -1
        #2
        data_res = []
        for i in datas:
            data_res.append(float(i[1]))
        pre_list = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.66,0.7,0.75,0.8,0.85,0.90,0.95,0.98,0.99,1]
        data_res = self.static.percentage_avg(data_res, pre_list)
        com = "percentage,use_time"
        save_percentage_fp = self.save_log(data_res, com, fp, save_dir)
        #assert 1 == 0
        #3
        xy_res = self.processt.sta_sec(datas)
        if 1 == is_change_to_second:
            sta_time = self.change_time_to_second(sta)
            end_time = self.change_time_to_second(end)
        else:
             sta_time = int(int(sta)/1000)
             end_time = int(int(end)/1000)

#            if None != sta:
#                sta_time = int(int(sta)/1000)
#            else:
#                sta_time = None
#            if None != end:
#                end_time = int(int(end)/1000)
#            else:
#                end_time = None
        xy_res = self.range_time(xy_res, [sta_time, end_time])
        x_u, y_u, max_u, std_u = self.time_statistics_dic_list(xy_res)
        save_fp= self.save_csv([self.datetime_from_second(x_u),y_u, max_u, std_u], fp, save_dir)
        print save_fp

        #x_u, y_u= self.processt.use_time_second(xy_res)
        #print self.save_csv([self.datetime_from_second(x_u),y_u], fp)

        yl = y_u
        res = self.statistics_list(yl)
        dl = {"Max(microsecond)":res[0], "Min(microsecond)":res[1] , "num": res[2], "avg": res[3], "stdev": res[4]}
        print dl
        return save_fp, res, save_percentage_fp
   
    def save_log(self, data_res, row, fp, save_dir):
        com = row
        for i in data_res:
            com = "%s\n%s,%s" % (com, str(i[0]), str(i[1]))
        if None == save_dir:
            use_fp = "test.log"
            res_fp = "test.log"
        else:
            fp = fp.split("/")[-1]
            use_fp = "%s/%s_percentage_avg.log" % (save_dir, str(fp))
            res_fp = "%s/%s_percentage_avg.log" % (save_dir, str(fp))
            self.log(use_fp)
        f=open(use_fp, "w")
        f.write(com)
        f.close()
        return res_fp 

    def range_time(self, s_sta, rt):
        sta = rt[0] if None != rt[0] else 0
        end = rt[1] if None != rt[1] else 9999999999999999
        source = copy.deepcopy(s_sta)
        for key in source:
            if "0" == key: #初始化的时间不做处理
                continue 
            self.log("[sta: %s, end: %s]key %s range_time" % (str(sta), str(end), str(key)))
            if float(sta) <= float(key) <= float(end):
                pass
            else:
                s_sta.pop(key)
        return s_sta
    
    def change_time_to_second(self, time_s):
        if None == time_s :
            return time_s
        listt = time_s.split(",")
        dt = datetime.datetime(int(listt[0]), int(listt[1]), int(listt[2]), int(listt[3]), int(listt[4]),int(listt[5]))
        return time.mktime(dt.timetuple())


    def time_statistics_dic_list(self, s_sta):
        x_res = []
        avg_res = []
        max_res = []
        std_res = []
        for sec in s_sta:
            res = self.statistics_list(s_sta[sec], key=1)
            self.log("res %s time_statistics_dic_list" % str(res))
            #assert 1 == 0
            x_res.append(sec)
            avg_res.append(res[3])
            max_res.append(res[0])
            std_res.append(res[4])

        return x_res, avg_res, max_res, std_res

    def statistics_list(self, dlist, key=-1):
        if -1 == key :
            pass
        else:
            new_list = []
            for i in dlist:
                new_list.append(i[key])
            dlist = new_list
        #self.log("(%s) statistics_list" % str(dlist))
        Max = max(dlist)
        Min = min(dlist)
        num = len(dlist)
        avg = sum(dlist) / num
        sdsq = sum([(i - avg) ** 2 for i in dlist])
        if 0 == ((len(dlist) - 1)) :
            stdev = 0
        else:
            stdev = (sdsq / (len(dlist) - 1)) ** .5
        return float(Max), float(Min), num, float(avg), float(stdev)

    def log(self, mes , leve=0):
        if leve >= DEFLOG:
            print "[ana_rttx] %s" % str(mes)

    def datetime_from_second(self, seconds_list):
        res = []
        for i in seconds_list:
            new_t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i))
            res.append(new_t)    
        return res 

    def save_csv(self, xy_list, fp, save_dir):
        x = xy_list[0]
        y = xy_list[1]
        z = xy_list[2]
        a = xy_list[3]
        com = "time,rtt_max,rtt_avg_use_time,rtt_std"
        index = 0
        for i in x:
            com = "%s\n%s,%s,%s,%s" % (com, str(i), str(z[index]), str(y[index]), str(a[index]))
            index = index + 1
        if None == save_dir:
            pass
        else:
            fp = fp.split("/")[-1]
            fp = "%s/%s" % (save_dir, str(fp))
        self.log(fp)
        f = open("%s.csv" % fp, "w")
        f.write(com)
        f.close()
        return "%s.csv" % fp
if __name__=="__main__":
    dp=sys.argv[1]
    dir=sys.argv[2]
    modfile=sys.argv[3]
    #except IndexError:
    #     dp="testdata/test.back"
    x = ana_rtt()
    #print x.doing(dp, None, None, "../testdata/")
    print dp
    res = x.doing(dp, None, None, dir)
    res_str = "csv:%s\ncsv:%s\ntabledata:ue_rtt:%s" % (res[0],res[2],res[1])
    print res_str
    f =open(modfile, "a")
    f.write(res_str)
    f.close()
