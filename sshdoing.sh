#!/bin/bash
#提供基础的ssh命令使用
#要求监控主机安装sshpass，
#被监控主机安装sysstat
#运行结果分析 stat.split.sh
source stat.split.sh

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
test_use(){

    ssh_all 1 slim password 192.168.1.114 &
    ssh_all 1 slim password 192.168.1.113 &
    ssh_all 1 slim abc123,./ 192.168.1.212 &
}
L2_use(){
    ssh_all 1 slim abc123,./ 192.168.1.80 &
    ssh_all 1 slim abc123,./ 192.168.1.207 &
    ssh_all 1 slim abc123,./ 192.168.1.73 &
    ssh_all 1 slim abc123,./ 192.168.1.74 &
    ssh_all 1 slim password 192.168.1.113 &
    ssh_all 1 slim password 192.168.1.114 &
    ssh_all 1 slim abc123,./ 192.168.1.212 &
    ssh_all 1 slim password 172.16.101.3 &
    ssh_all 1 slim password 192.168.1.56 &
    ssh_all 1 slim password 192.168.1.58 &
}
main(){
    savedir=$1
    logbdir="logback"
    ssh_monitor 120
    test_stat "${logbdir}" "${savedir}" "iostat"
    test_stat "${logbdir}" "${savedir}" "mpstat"
    test_stat "${logbdir}" "${savedir}" "vmstat"
}
main $1
