#!/bin/bash
log_time(){
    # noc 屏幕输出time格式化dygraphs使用
    log=$1
    cat ${log}|sed 's/\([0-9][0-9]\)\([0-9][0-9]\)\([0-9][0-9]\)\([0-9][0-9]\)\([0-9][0-9]\)/2017-\1-\2 \3:\4:\5/g'>${log}_tmp
    mv ${log}_tmp ${log}
}
std_log_time(){
    # noc 屏幕输出time格式化dygraphs使用
    log=$1
    cat ${log}|sed 's/^\([0-9]\{4\}\)\([0-9][0-9]\)\([0-9][0-9]\)\([0-9][0-9]\)\([0-9][0-9]\)\([0-9][0-9]\)/\1-\2-\3 \4:\5:\6/g'>${log}_tmp
    mv ${log}_tmp ${log}
}
test(){
    #log_time $1
    std_log_time $1
    cat $1
}
test $1
