#!/bin/bash
get_html(){
    ip=$1
    savedir=$2
    ngdir=$3
    saveindexlog=$4
    fplist=`python html/activity_mod.py ${ip} ${savedir}`
    mv ${fplist} ${ngdir}
    for fp in ${fplist}
    do
        echo "http://192.168.1.216/spotlight_web/${fp}"
        echo "http://192.168.1.216/spotlight_web/${fp}">>${saveindexlog}
    done
}
L2_host(){
    iplist="192.168.1.80 192.168.1.207 192.168.1.73 192.168.1.74 192.168.1.113 192.168.1.114 192.168.1.212 172.16.101.3 192.168.1.56 192.168.1.58"
    ngdir="/data2/spotlight_web"
    mv $1 ${ngdir}
    for i in ${iplist}
    do
        get_html $i $1 ${ngdir} $2
    done
    
}
Load_test_host(){
    iplist="192.168.1.80 192.168.1.207 192.168.1.84 192.168.1.113 192.168.1.114 192.168.1.99 192.168.1.208 192.168.1.212 172.16.101.3 192.168.1.56 192.168.1.58"
    ngdir="/data2/spotlight_web"
    mv $1 ${ngdir}
    for i in ${iplist}
    do
        get_html $i $1 ${ngdir} $2
    done
}
Relay_test_host(){
    iplist="192.168.1.80 192.168.1.207 192.168.1.84 192.168.1.113 192.168.1.73 192.168.1.74 192.168.1.75 192.168.1.76 192.168.1.114 192.168.1.99 192.168.1.208 192.168.1.212 172.16.101.3 192.168.1.56 192.168.1.58"
    ngdir="/data2/spotlight_web"
    mv $1 ${ngdir}
    for i in ${iplist}
    do
        get_html $i $1 ${ngdir} $2
    done
}
write_table(){
    fgw="192.168.1.73 192.168.1.74 192.168.1.113"
    bgw="192.168.1.114"
    app="192.168.1.212"
    ue="192.168.1.80 192.168.1.207"
    relay="192.168.1.56 192.168.1.58"
    mysql="172.16.101.3"
    #list_table="${fgw} ${bgw} ${app} ${ue} ${relay} ${mysql}"
    loglist=$1
    

    
}

#L2_host 201704261918 
