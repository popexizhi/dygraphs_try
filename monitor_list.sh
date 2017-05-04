#!/bin/bash
#要求监控主机列表
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
Load_test_use(){
    ssh_all 1 slim abc123,./ 192.168.1.80 &
    ssh_all 1 slim abc123,./ 192.168.1.84 &
    ssh_all 1 slim abc123,./ 192.168.1.207 &
    ssh_all 1 slim password 192.168.1.113 &
    ssh_all 1 slim password 192.168.1.114 &
    ssh_all 1 slim password 192.168.1.99 &
    ssh_all 1 slim abc123,./ 192.168.1.212 &
    ssh_all 1 slim abc123,./ 192.168.1.208 &
    ssh_all 1 slim password 172.16.101.3 &
    ssh_all 1 slim password 192.168.1.56 &
    ssh_all 1 slim password 192.168.1.58 &
}
