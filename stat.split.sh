#!/bin/bash
#用于分隔*stat文件中的内容
#
split_iostat(){
    fp=$1
    time=`cat ${fp}|head -n 1`
    filelist=`cat ${fp}|sed 's/^$/time+1/g'|grep -v "Device:"|grep -v CPU|sed 's/ \+/,/g'`
    for i in ${filelist}
    do
        echo "${i}"
    done
}


test(){
    split_iostat logback/192.168.1.113__iostat
}
test 
