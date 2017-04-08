#!/bin/bash
ep_throughput(){

    cat ${log}|grep "EpollLoop Throughput statistic"|sed 's/^\[[0-9]\+://g'|sed 's/:.*sent=/,/g'|sed 's/(.*=/,/g'|sed 's/(kb)//g'

}

has_fush(){
#
	echo "$1i---logpre is $2"
	logpre=$2
	file_num=`cat $1|grep ${logpre}|grep -v std|wc -l`
	if ((${file_num}>1))
	then
		echo "$logpre is more"
	else
		echo "one "
	fi
	
}
has_fush tlog app
has_fush tlog bgw
