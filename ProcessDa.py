# -*- coding:utf8 -*-
import os, re
import collections
import time
class ProcessDa():
    def sta_sec(self, list_data):
        """
        list_data 以第一列数据为索引排序后,按秒钟分类结果返回
        """
        print "[sta_sec]sta..."
        list_data.sort() #要求list_data中以毫秒为存储单位
        #print list_data
        if len(list_data) == 0:
            return [] 
        old_d = list_data[0]
        j = 0
        s_sta = {}
        #2.将新值加入到s_stat
        s_sta[int(old_d[0])/1000] = []
        s_sta[int(old_d[0])/1000].append(old_d)

        for i in list_data[1:]:
            #print "*" *20
            #print i
            j = j + 1
            if self.if_same_sec(int(i[0]), int(old_d[0])):
                #同一计数单位，存储
                #print "key is %s" % str(int(old_d[0]/1000))
                s_sta[int(int(old_d[0])/1000)].append(i) 
                
            else:
                #1.记录新的old_d
                old_d = i
                #2.将新值加入到s_stat
                s_sta[int(int(old_d[0])/1000)] = []
                s_sta[int(int(old_d[0])/1000)].append(i)
    
        s_sta = collections.OrderedDict(sorted(s_sta.items())) #按key对dist排序
        #for key in s_sta:
        #    print key
        #    print s_sta[key]
            #print "%s : %s" % (str(key), str(value))
        print "[sta_sec]end..."
        return s_sta
    
    def if_same_sec(self, now_s, def_s):
        res = ( int(def_s/1000) == int(now_s/1000) )
        return res

    def file2matrix(self, filename):
        """
            open file 
        """
        print "[file2matriz]sta..."
        fr = open(filename)
        arrayOLlines_len = len(fr.readlines())
        if 0 == arrayOLlines_len:
            print "%s is null" % filename
            return -1
        print "arrayOLlines_len %s" % str(arrayOLlines_len)
        returnMat = [] #numpy.zeros((arrayOLlines_len, 4))
        index = 0
        diff_time = 0#92000 # appserver 与ue的server时间差, 单位:毫秒
        fr = open(filename)
        for line in fr.readlines():
            line = line.split("\n")[0]
            listFromline = line.split(",")
            if len(listFromline) < (2-1): # numpy.zeros 初始化时的形状要求，如果小于这个值，说明数据不完整
                continue
            if len(re.findall(u"\D", listFromline[0]))> 0 or len(re.findall(u"\D", listFromline[1]))> 0 : #行数据不完整,忽略此内容
                listFromline[1] = listFromline[1].split(" ")[0] #处理结尾的空格
                if len(re.findall(u"\D", listFromline[0]))> 0 or len(re.findall(u"\D", listFromline[1]))> 0 : #行数据不完整,忽略此内容
                    print "(%s) \\D" % str(listFromline)
                    continue
                else:
                    pass #继续处理
            listFromline_res = [listFromline[0], listFromline[1], 0, 0]
            listFromline_res[1] = int(listFromline_res[0]) - int(listFromline_res[1]) + diff_time #use_time = receive_time - send_time + diff_time
            
            returnMat.append(listFromline_res)
            index +=1

        fr.close()
        print "[file2matriz]end..."
        return returnMat
if __name__=="__main__":
    x = ProcessDa()
    sta1 = time.time()
    data = x.file2matrix("testdata/test.back")
    print "end file2matrix"
    sta2 = time.time()
    x.sta_sec(data)
    end = time.time()
    print "openfile:%f; sta_sec:%f" % ((sta2-sta1), (end-sta2))
