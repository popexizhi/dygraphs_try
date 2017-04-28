#!/bin/bash
get_html(){
    ip=$1
    savedir=$2
    ngdir=$3
    fplist=`python html/activity_mod.py ${ip} ${savedir}`
    mv ${fplist} ${ngdir}
    for fp in ${fplist}
    do
        echo "http://192.168.1.216/spotlight_web/${fp}"
    done
}
L2_host(){
    iplist="192.168.1.80 192.168.1.207 192.168.1.73 192.168.1.74 192.168.1.113 192.168.1.114 192.168.1.212 172.16.101.3 192.168.1.56 192.168.1.58"
    ngdir="/data2/spotlight_web"
    mv $1 ${ngdir}
    for i in ${iplist}
    do
        get_html $i $1 ${ngdir}
    done
}

#L2_host 201704261918 
