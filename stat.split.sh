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

split_mpstat(){
    fp=$1
    time=`cat ${fp}|head -n 1`
    #filelist=`cat ${fp}|sed 's/^$/time+1/g'|grep -v "Device:"|grep -v CPU|sed 's/ \+/,/g'|sed 's/^[0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\},..,//g'` 
    filelist=`cat ${fp}|sed 's/^$/time+1/g'|grep -v "Device:"|grep -v CPU|sed 's/ \+/,/g'|sed 's/^\([0-9]\{2\}.*秒,\)\|\([0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\},...\?,\)//g'` 
    for i in ${filelist}
    do
        echo "${i}"
    done
}

split_vmstat(){
    fp=$1
    time=`cat ${fp}|head -n 1`
    filelist=`cat ${fp}|grep -v "procs"|grep -v "free"|sed 's/^[0-9]\?\+ /time+1\nvmstat &/g'|sed 's/ \+/,/g'` 
    for i in ${filelist}
    do
        echo "${i}"
    done
}
test_iostat(){
    dir=$1
    resdir=$2
    filelist=`ls -all ${dir}|grep _iostat$|awk '{print $9}'`
    for i in ${filelist}
    do
        echo "~~~~~~~~~~~~~~~$i~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        split_iostat ${dir}/${i}|tee ${dir}/${i}_tmp
        mkdir ${resdir}/${i}
        python Sp2Csv.py ${dir}/${i}_tmp ${resdir}/${i} "iostat"
    done
}
test_stat(){
    dir=$1
    resdir=$2
    stat=$3
    echo "[test_stat]: -${dir}-${resdir}-${stat}"
    filelist=`ls -all ${dir}|grep _${stat}$|awk '{print $9}'`
    echo "[test_stat]: filelist--${filelist}"
    for i in ${filelist}
    do
        echo "~~~~~~~~~~~~~~~$i~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        #split_mpstat ${dir}/${i}|tee ${dir}/${i}_tmp
        split_${stat} ${dir}/${i}|tee ${dir}/${i}_tmp
        mkdir ${resdir}/${i}
        python Sp2Csv.py "${dir}/${i}_tmp" "${resdir}/${i}" "${stat}"
    done
}
test_all(){
    test_iostat logback "/data2/spotlight_web/iostat"
    test_stat logback "/data2/spotlight_web/mpstat" mpstat
    test_stat logback "/data2/spotlight_web/vmstat" vmstat
}

#test_iostat logback I iostat
#split_mpstat logback/172.16.101.3__mpstat 
#split_mpstat logback/192.168.1.113__mpstat 
