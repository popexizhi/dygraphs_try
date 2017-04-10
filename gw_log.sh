#!/bin/bash
ep_throughput(){

    cat ${log}|grep "EpollLoop Throughput statistic"|sed 's/^\[[0-9]\+://g'|sed 's/:.*sent=/,/g'|sed 's/(.*=/,/g'|sed 's/(kb)//g'

}
