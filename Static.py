#-*-coding:utf8-*-

class static():
    def statistics_list(self, dlist):
        Max = max(dlist)
        Min = min(dlist)
        num = len(dlist)
        avg = sum(dlist) / num 
        sdsq = sum([(i - avg) ** 2 for i in dlist])
        if 1 == num:
            stdev = 0.0
        else:
            stdev = (sdsq / (len(dlist) - 1)) ** .5
        return float(Max), float(Min), float(num), float(avg), float(stdev)
    def quartiles(self, dlist):
        dlist.sort()
        sort_d = dlist
        num = len(dlist)-1

        if 0 == num%2:
            med = sort_d[int(num/2)]
            q1 = sort_d[int(num/4)]
            q3 = sort_d[ num-int(num/4)]
        else:
            med = sort_d[int(num/2)] * 0.5 + sort_d[int(num/2)+1] * 0.5
           
            res = self.ff(float(num*1.0/4))
            q1_i = int(res[0])
            q1_d = float(res[1])
            q1 = sort_d[q1_i] * (1.0-q1_d) + sort_d[q1_i+1] * q1_d

            res = self.ff(float(num*1.0*3/4))
            q3_i = int(res[0])
            q3_d = float(res[1])
            q3 = sort_d[q3_i] * q3_d + sort_d[q3_i + 1] * (1.0-q3_d)
        return q1, med , q3

    def percentage_avg(self, dlist, per_list):
        dlist.sort()
        percentage_rec = []
        for x in per_list:
            num = int(len(dlist) * float(x))
            print num
            print dlist
            #res = self.statistics_list(dlist[0:num]) #float(Max), float(Min), float(num), float(avg), float(stdev)
            res = dlist[num-1]
            percentage_rec.append([x, res])
        return percentage_rec
    def ff(self, data):
        integer = int(data)
        decimal = data*1.0 - integer

        return integer, decimal


    def log(self, mes):
        print "[Static] %s" % str(mes)

    def static_second_num(self, list_list):
        res_list = []
        data_res = []
        if 0 == len(list_list):
            return res_list
        old = list_list[0][0]
        old_count = 1
        for i in list_list:
            if i[0] == old:
               old_count = old_count + 1 
            else:
               res_list.append([old, old_count])
               data_res.append(old_count)
               old = i[0]
               old_count = 1

        return res_list, data_res

    def statistics_list_avg(self, list_l):
        """对list_l 按[0]排序统计后，返回[1]的统计结果 """
        res = []
        if 0 == len(list_l):
            return res
        list_l = self.sort_list_l(list_l) #对list_l 按[0] 排序
        static_res = []
        arg_res = []
        old = list_l[0][0]
        old_res = []
        old_res.append(float(list_l[0][1]))
        for i in list_l[1:]:
            if i[0] == old:
                old_res.append(float(i[1]))
            else:
                #旧数据处理
                print old_res
                ss = self.statistics_list(old_res) #float(Max), float(Min), float(num), float(avg), float(stdev)
                res.append([old, ss[2], ss[-2],ss[0], ss[-1]]) #arg, max, std
                static_res.append(ss[2])
                arg_res.append(ss[-2])
                #存新数据
                old = i[0]
                old_res = []
                old_res.append(float(i[1]))
                
        ss = self.statistics_list(old_res)
        res.append([old, ss[2], ss[-2],ss[0], ss[-1]]) #arg, max, std
        static_res.append(ss[2])
        arg_res.append(ss[-2])
        return res, static_res, arg_res
    def sort_list_l(self, list_l, sort_id=0):
        """对list_l按sort_id指定位置升序 """
        list_key ={}
        res_list=[]
        for i in list_l:
            new_key = i[sort_id]
            print new_key
            if list_key.has_key(new_key):
                list_key[new_key].append(i)
            else:
                list_key[new_key] = [i]
        
        for j in sorted(list_key.iterkeys()): #按key 升序字典
            #print j
            for t in list_key[j]:
                res_list.append(t)
                #print "\t\t%s" % str(res_list)
        return res_list
if __name__ == "__main__":
    x = static()
    print x.quartiles([83, 82, 86, 84, 87, 79, 81, 85, 82, 92])
    print x.quartiles([13,13.5,13.8,13.9,14,14.6,14.8,15,15.2,15.4,15.7])
    print x.quartiles([13,13.5,13.8,13.9,14,14.6,14.8,15,15.2,15.4])
