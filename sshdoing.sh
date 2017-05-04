#!/bin/bash
#提供基础的ssh命令使用
#要求监控主机安装sshpass，
#被监控主机安装sysstat
#运行结果分析 stat.split.sh
source stat.split.sh
source savehtml.sh
source monitor_list.sh

ssh_iostatX(){
    time_space=$1
    user=$2
    passwd=$3
    ip=$4
    backdir="logback"
    echo "start ${ip} iostat"
    sshpass -p "${passwd}" ssh ${user}@${ip} "iostat -x -d -k ${time_space}">${backdir}/${ip}_io     
}

ssh_doing(){
    time_space=$1
    user=$2
    passwd=$3
    ip=$4
    backdir="logback"
    cmd_str=$5
    log_pre=$6
    echo "start ${ip} ${cmd_str}"
    sshpass -p "${passwd}" ssh ${user}@${ip} "date +'%F %T'">${backdir}/${ip}_${log_pre} 
    sshpass -p "${passwd}" ssh ${user}@${ip} "echo ${time_space}">>${backdir}/${ip}_${log_pre} 
    sshpass -p "${passwd}" ssh ${user}@${ip} "${cmd_str} ${time_space}">>${backdir}/${ip}_${log_pre} 
}

ssh_iostat(){
    ssh_doing $1 $2 $3 $4 "iostat -x -d -k " "_iostat"
}
ssh_cpu(){
    ssh_doing $1 $2 $3 $4 "mpstat -P ALL " "_mpstat"
}
ssh_memory(){
    ssh_doing $1 $2 $3 $4 "vmstat " "_vmstat"
}

stop(){
    grep_cmd=$1
    echo "stop ${grep_cmd}"
    ps -ef|grep ${grep_cmd}|grep -v grep|awk '{print "pid:$2,$9";system("kill -9 "$2)}'
}
ssh_all(){
    ssh_doing $1 $2 $3 $4 "iostat -x -d -k " "_iostat" &
    ssh_doing $1 $2 $3 $4 "vmstat " "_vmstat" &
    ssh_doing $1 $2 $3 $4 "mpstat -P ALL " "_mpstat" &
}
ssh_monitor(){
    runtime=$1
    #test_use
    L2_use
    echo "wait "
    sleep ${runtime}
    stop iostat
    stop mpstat
    stop vmstat
}

main(){
    savedir=`date +%Y%m%d%H%M%s`
    logdir="logback"
    echo "savedir:${savedir}" 
    mkdir ${savedir}
    rm -rf ${logdir}
    mkdir ${logdir}
    ssh_monitor $1
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~start get csv file"
    test_stat "${logdir}" "${savedir}" "iostat"
    test_stat "${logdir}" "${savedir}" "mpstat"
    test_stat "${logdir}" "${savedir}" "vmstat"

    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~start get html report"
    echo "${savedir} html res">${savedir}.log
    L2_host ${savedir} ${savedir}.log
}
main $1
