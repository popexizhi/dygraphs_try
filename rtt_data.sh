#!/bin/bash
uelog2rtt(){
#从uelog过滤全部的rtt使用
    ue_log=$1
    old_dir=$2
    new_dir=$3
    echo ${old_dir}/${ue_log}
    echo ${new_dir}/${ue_log}
    echo "rtt***************************"
    cat ${old_dir}/${ue_log}|grep "Tcp Model recv ping now:"|sed 's/^.*ping now://g'|sed 's/,content: Ping packet [0-9][0-9]* ,ue send tm /,/g'>${new_dir}/${ue_log}_rtt
    echo "********************************************"
    #cat ${new_dir}/${ue_log}_rtt
}
dirlog(){
    #从dir中过滤全部log特征名称的loglist,追加全部内容到$4中
    dir=$1
    logpre=$2
    desdir=$3
    resfile=$4
    loglist=`ls -all ${dir}|grep ${logpre}|awk '{print $9}'`
    echo "ls -all ${dir}|grep ${logpre}|awk '{print $9}'"
    for i in ${loglist}
    do
        uelog2rtt $i ${dir} ${desdir}
        cat ${desdir}/${i}_rtt>>${resfile}
    done
    echo "${resfile} has lines:"
    cat ${resfile}|wc -l
}
test(){
    dirlog "../bgw_restart_quickly/uelog/" "log.txt" "testdata/test" "testdata/test.rttd" 
    echo "start rtt 分析"
    python ana_rtt.py "testdata/test.rttd"
}
main(){
    #处理uelog过程
    uelog=$1
    resdir=$2
    resrttfile=$3
    echo 'dirlog "${uelog}" "log.txt" "${resdir}" "${resrttfile}" '
    dirlog "${uelog}" "log.txt" "${resdir}" "${resrttfile}" 
    echo "start rtt 分析"
    python ue_rtt/ana_rtt.py "${resrttfile}"
}
main $1 $2 $3
#test
