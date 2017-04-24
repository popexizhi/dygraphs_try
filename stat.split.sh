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
    dir=$1
    filelist=`ls -all ${dir}|grep iostat$|awk '{print $9}'`
    for i in ${filelist}
    do
        echo "~~~~~~~~~~~~~~~$i~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        split_iostat ${dir}/${i}|tee ${dir}/${i}_tmp
    done
}
test logback 
