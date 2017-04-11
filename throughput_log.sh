#!/bin/bash
source log_csv.sh
source rtt_data.sh
get_csv(){
    resfp=$1        #log所在文件夹
    grep_kind=$2    #log类型
    fp_list=`ls -all ${resfp}|grep throughput|grep -v csv|awk '{print $9}'` #appserver log文件列表
    for i in ${fp_list}
    do
        #echo "time,throughput(Kbps)">${resfp}/$i.csv
        #cat ${resfp}/$i|sed 's/^\[[0-9]\+://g'|sed 's/:.* KiB \/ s//g'|sed 's/Kbps//g'|sed 's/ //g'>>${resfp}/$i.csv #Kbps
        echo "get_grep ${grep_kind} ${resfp}/$i"
        get_grep ${grep_kind} ${resfp}/$i 

        echo ${resfp}/$i.csv
    done 
}

get_grep(){
    echo "[get_grep]---log_kind:$1--原始位置:$2"
    log_kind=$1 #log类型，当前支持appserver log的throughput; 
                #         nohup中显示的connected client数量
                #         epollLoop_throughput -- EpollLoop Throughput statistic
    fp=$2       #原始log的文件名称
    case $1 in
    "throughput" ) #appserver log的throughput
        echo "time,throughput(Kbps)">${fp}.csv
        cat ${fp}|sed 's/^\[[0-9]\+://g'|sed 's/:.* KiB \/ s//g'|sed 's/Kbps//g'|sed 's/ //g'>>${fp}.csv #Kbps
        ;; 
   "connected_client" )
        echo "time,connected_client">${fp}.csv
        cat ${fp}|sed 's/ .*: /,/g'|sed 's/\[//g'|sed 's/-.\{2\}.\?:.\{2\}.\?\]//g'|grep -v "start\|change,soft"|grep "^2[0-9]\{3\}-"|sed 's/-//g'|sed 's/^[0-9]\{8\}/&\//g'>>${fp}.csv
        ;;
   "epollLoop_throughput" )
        echo "time,epollLoop_sent(kb),epollLoop_read(kb)">${fp}.csv
        cat ${fp}|grep "EpollLoop Throughput statistic"|sed 's/^\[[0-9]\+://g'|sed 's/:.*sent=/,/g'|sed 's/(.*=/,/g'|sed 's/(kb)//g'>>${fp}.csv
        ;;
   *)
        echo "no has this log GREP Kind"
        return -1
        ;;
   esac

   return 0
}

save_app_log(){
    echo "save app log... server_log_dir:$1- 结果存储dir$2"
    server_log_dir=$1    #原始log位置
    ph=$2                #结果存储位置
    res_des=$2/app_log.html_mod   #结果描述存储位置
    echo "title:app_server_downlink">${res_des}
    echo "testtime:`date +%y-%m-%d-%H-%M`">>${res_des}

    app_log_list=`ls -all ${server_log_dir}|grep app_server_|grep -v std_out|grep -v csv|grep -v ".swp"|awk '{print $9}'`
    file_num=`ls -all ${server_log_dir}|grep app_server_|grep -v std_out|grep -v csv|wc -l`
    echo "destabledata:app_log:${file_num}">>${ph}/res.log
    echo "iframe_list:app_server_downlink.html">>${ph}/res.log
    for app_log in ${app_log_list}
    do 
        server_log=${server_log_dir}/${app_log}
        cat ${server_log} |grep throughput|grep TCP|grep downlink>${ph}/${app_log}_tcp_throughput_downlink.log
        cat ${server_log} |grep throughput|grep TCP|grep uplink>${ph}/${app_log}_tcp_throughput_uplink.log
        get_csv ${ph} "throughput" #过滤appserver的throughput
        version=`cat ${server_log}|grep version=|sed 's/.*version=//g'|sed 's/:.*//g'|sort |uniq|xargs echo "version:"`
        echo "${app_log}---version:${version}"
        echo "des:cluster_app_server(version:${version})">>${res_des}
   done
   fush_log ${ph} "app_log.html_mod" 
}

save_app_std(){
    echo "save app std output...server log dir :$1-目标文件位置:$2"
    server_log_dir=$1   #原始log位置
    ph=$2           #结果存储位置
    res_des=$2/app_std.html_mod   #结果描述存储位置
    echo "title:app_server_std">${res_des}
    echo "testtime:`date +%y-%m-%d-%H-%M`">>${res_des}

    fp_list=`ls -all ${server_log_dir}|grep app_server_|grep std_out|grep -v csv|grep -v ".swp"|awk '{print $9}'` #appserver log文件列表
    fp_num=`ls -all ${server_log_dir}|grep app_server_|grep std_out|grep -v csv|wc -l`  #appserver log文件列表
    echo "destabledata:app_std:${fp_num}">>${ph}/res.log
    echo "iframe_list:app_server_std.html">>${ph}/res.log
    for i in ${fp_list}
    do
        echo "app std output file ${server_log_dir}/$i"
        get_grep "connected_client" ${server_log_dir}/$i
        mv ${server_log_dir}/$i.csv ${ph}
    done 
    app_server_log_list=`ls -all ${fpdir}|grep csv|grep app_server|grep std_out|awk '{print $9}'|sed ':a;N;$!ba;s/\n/ /g'`
    fush_log="app_server_std_out_fush.file"
    fush_fp ${ph} "app_std.html_mod" "${app_server_log_list}" "${fush_log}"
}

fush_log(){
    echo "reaapp log is $1;resfp $2"
    fpdir=$1
    resfp=$2
    app_server_log_list=`ls -all ${fpdir}|grep csv|grep app_server|grep -v std_out|grep downlink|awk '{print $9}'|sed ':a;N;$!ba;s/\n/ /g'`
    app_server_downlink_fush_log="app_server_log_fush.file"
    echo ${app_server_log_list} ${app_server_downlink_fush_log}
    echo "csv:${app_server_downlink_fush_log}">>${fpdir}/${resfp}
    echo "python ../fuselog/FuseCsv.py ${app_server_log_list} ${app_server_downlink_fush_log}"
    cur_dir=`pwd`
    cd ${fpdir}&&python ../fuselog/FuseCsv.py ${app_server_log_list} ${app_server_downlink_fush_log} ${resfp}
    python ../report/Report.py ${resfp}
    cd ${cur_dir}
}
fush_fp(){
    echo "reaapp log is $1;resfp $2;log_list $3;fush_log $4"
    fpdir=$1
    resfp=$2
    log_list=$3
    fush_log=$4
    echo "csv:${fush_log}">>${fpdir}/${resfp}
    echo "python ../fuselog/FuseCsv.py ${log_list} ${fush_log}"
    cur_dir=`pwd`
    cd ${fpdir}
    ls -all .
    python ../fuselog/FuseCsv.py ${log_list} ${fush_log} ${resfp}
    python ../report/Report.py ${resfp}
    cd ${cur_dir}
}

test(){
    #fush_log $1 
    
    #mkdir test
    save_gw_std nag_normal_online test
    #save_gw_std cluster_normal_online test

    #get_grep "epollLoop_throughput" bgw.log.txt_192.168.1.114 
    #has_fush $1
}
save_gw_std(){
    echo "save gw log... gw_log_dir:$1- 结果存储dir $2"
    server_log_dir=$1    #原始log位置
    ph=$2                #结果存储位置
    res_des=$2/res   #结果描述存储位置
    gw_log_list=`ls -all ${server_log_dir}|grep gw_|grep std_out|grep -v csv|awk '{print $9}'`
    echo "gw_log_list is ${gw_log_list}"
    for gw_std in ${gw_log_list}
    do
        get_grep "connected_client" ${server_log_dir}/${gw_std}
        echo "${gw_std}.csv">>${res_des}.csvfiles
    done
    mv ${server_log_dir}/*.csv ${ph}
    #fush ?
    bgw_num=`echo "${gw_log_list}"|grep bgw|wc -l`
    
    htmlmod="bgw_std.html_mod"	
    echo "bgw_num:${bgw_num}"
    echo "title:bgw_std">${ph}/${htmlmod}
    echo "des:bgw_std">>${ph}/${htmlmod}
    echo "testtime:`date +%y-%m-%d-%H-%M`">>${ph}/${htmlmod}

    echo "destabledata:bgw_std:${bgw_num}">>${ph}/res.log
    echo "iframe_list:bgw_std.html">>${ph}/res.log
    if ((${bgw_num}>1))
    then
	echo "bgw need fulsh: ${bgw_num}" 
	log_list=`echo "${gw_log_list}"|grep bgw|sed 's/$/.csv/g'|sed ':a;N;$!ba;s/\n/ /g'`
	fush_log="bgw_std_out_fush.file"
    	fush_fp ${ph} "${htmlmod}" "${log_list}" "${fush_log}"
    else
	    echo "bgw only one "
	    log_list=`echo "${gw_log_list}"|grep bgw|sed 's/$/.csv/g'`
        echo "csv:${log_list}">>${ph}/${htmlmod}
	    python fuselog/StaticCsv.py "${ph}/${log_list}" "${ph}/${htmlmod}" #tabledata
	    cur=`pwd`
        cd ${ph}&&python ../report/Report.py ${htmlmod}
	    cd ${cur}
    fi

    fgw_num=`echo "${gw_log_list}"|grep fgw|wc -l`
    htmlmod="fgw_std.html_mod"	
    echo "title:fgw_std">${ph}/${htmlmod}
    echo "des:fgw_std">>${ph}/${htmlmod}
    echo "testtime:`date +%y-%m-%d-%H-%M`">>${ph}/${htmlmod}
    echo "destabledata:fgw_std:${fgw_num}">>${ph}/res.log
    echo "iframe_list:fgw_std.html">>${ph}/res.log
    if ((${fgw_num}>1))
    then
	echo "fgw need fulsh: ${fgw_num}" 
	log_list=`echo "${gw_log_list}"|grep fgw|sed 's/$/.csv/g'|sed ':a;N;$!ba;s/\n/ /g'`
	fush_log="fgw_std_out_fush.file"
    	fush_fp ${ph} "${htmlmod}" "${log_list}" "${fush_log}"
    else
	    echo "fgw only one "
	    log_list=`echo "${gw_log_list}"|grep fgw|sed 's/$/.csv/g'`
        echo "csv:${log_list}">>${ph}/${htmlmod}
	    echo 'python fuselog/StaticCsv.py "${ph}/${log_list}" "${ph}/${htmlmod}" ' #tabledata
	    python fuselog/StaticCsv.py "${ph}/${log_list}" "${ph}/${htmlmod}" #tabledata
	    cur=`pwd`
    	cd ${ph}&&python ../report/Report.py ${htmlmod}
	    cd ${cur}
    fi

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

save_gw_log(){
    echo "save gw log... gw_log_dir:$1- 结果存储dir $2"
    server_log_dir=$1    #原始log位置
    ph=$2                #结果存储位置
    res_des=$2/res   #结果描述存储位置
    gw_log_list=`ls -all ${server_log_dir}|grep gw|grep -v std_out|grep -v csv|awk '{print $9}'`
    echo "gw_log_list is ${gw_log_list}"
    for gw_std in ${gw_log_list}
    do
        get_grep "epollLoop_throughput" ${server_log_dir}/${gw_std}
        echo "${gw_std}.csv">>${res_des}.csvfiles
    done
    mv ${server_log_dir}/*.csv ${ph}
    #fush ?
    bgw_num=`echo "${gw_log_list}"|grep bgw|wc -l`
    
    htmlmod="bgw_log.html_mod"	
    echo "bgw_num:${bgw_num}"
    echo "title:bgw_log">${ph}/${htmlmod}
    echo "des:bgw_log">>${ph}/${htmlmod}
    echo "testtime:`date +%y-%m-%d-%H-%M`">>${ph}/${htmlmod}

    echo "destabledata:bgw_log:${bgw_num}">>${ph}/res.log
    echo "iframe_list:bgw_log.html">>${ph}/res.log
    if ((${bgw_num}>1))
    then
	echo "bgw need fulsh: ${bgw_num}" 
	log_list=`echo "${gw_log_list}"|grep bgw|sed 's/$/.csv/g'|sed ':a;N;$!ba;s/\n/ /g'`
	fush_log="bgw_log_fush.file"
    	fush_fp ${ph} "${htmlmod}" "${log_list}" "${fush_log}"
    else
	    echo "bgw only one "
	    log_list=`echo "${gw_log_list}"|grep bgw|sed 's/$/.csv/g'`
        echo "csv:${log_list}">>${ph}/${htmlmod}
	    python fuselog/StaticCsv.py "${ph}/${log_list}" "${ph}/${htmlmod}" #tabledata
	    cur=`pwd`
    	cd ${ph}&&python ../report/Report.py ${htmlmod}
	    cd ${cur}
    fi
    fgw_num=`echo "${gw_log_list}"|grep fgw|wc -l`
    htmlmod="fgw_log.html_mod"	
    echo "title:fgw_log">${ph}/${htmlmod}
    echo "des:fgw_log">>${ph}/${htmlmod}
    echo "testtime:`date +%y-%m-%d-%H-%M`">>${ph}/${htmlmod}
    echo "destabledata:fgw_log:${bgw_num}">>${ph}/res.log
    echo "iframe_list:fgw_log.html">>${ph}/res.log
    if ((${fgw_num}>1))
    then
        echo "fgw need fulsh: ${fgw_num}" 
	    log_list=`echo "${gw_log_list}"|grep fgw|sed 's/$/.csv/g'|sed ':a;N;$!ba;s/\n/ /g'`
	    fush_log="fgw_log_fush.file"
    	fush_fp ${ph} "${htmlmod}" "${log_list}" "${fush_log}"
    else
	    echo "fgw only one "
	    log_list=`echo "${gw_log_list}"|grep fgw|sed 's/$/.csv/g'`
        echo "csv:${log_list}">>${ph}/${htmlmod}
	    python fuselog/StaticCsv.py "${ph}/${log_list}" "${ph}/${htmlmod}" #tabledata
	    cur=`pwd`
    	cd ${ph}&&python ../report/Report.py ${htmlmod}
	cd ${cur}
    fi
}
get_csv_time(){
    echo "dir is $1"
    dir=$1
    log_list=`cat ${dir}/*mod|grep csv|grep -v std_out|grep log|grep -v rtt|sed 's/csv://g'`
    for i in ${log_list}
    do
        log_time ${dir}/${i}
    done
    echo "log_time: ${log_list}"
    log_list=`cat ${dir}/*mod|grep csv|grep std_out|grep -v rtt|sed 's/csv://g'`
    for i in ${log_list}
    do
        std_log_time ${dir}/${i}
    done
    echo "std_time: ${log_list}"
    
}

main(){
    source_log_dir=$1
    echo "source log dir is ${source_log_dir}"
    ph="resapp_`date '+%y%m%d%H%M'`"
    mkdir ${ph}
    echo "title:${source_log_dir}">${ph}/res.log
    use_date=`date +%y-%m-%d-%H-%M`
    echo "testtime:${use_date}">>${ph}/res.log
    echo "des:cluster_test_${source_log_dir}">>${ph}/res.log
    save_app_log ${source_log_dir} ${ph} #收集结果并处理 $1 原始log位置 $2结果存储log的文件夹
    save_app_std ${source_log_dir} ${ph}        #收集结果并处理 $1 原始log位置 $2结果存储log的文件夹

    save_gw_std ${source_log_dir} ${ph} #fgw/bgw st_log 处理 
    save_gw_log ${source_log_dir} ${ph} #fgw/bgw st_out 处理 
    #ue log
    echo "sta ue log ......"
    #rtt_main "${source_log_dir}/uelog/" "${ph}" "${ph}/res.rttd" "${ph}/res.log"
    echo "end ue log ......"
    cat ${ph}/res.log
    #html
    python report/Report.py "${ph}/res.log" "${ph}"  #html report
    echo "http://192.168.1.216/test/provision_test/load_test/cluster/${source_log_dir}_${use_date}.html">"cluster_test_result_html.txt" #jenkins use file
    sleep 1
    get_csv_time ${ph}
    sshpass -p'abc123,./' scp *.html slim@192.168.1.216:/data/provision_test/load_test/cluster/
    sshpass -p'abc123,./' scp -r ${ph} slim@192.168.1.216:/data/provision_test/load_test/cluster/
    mv  *.html back
    mv  ${ph} back
    #rm -rf back
    #mkdir back
}
main $1
#cluster_test_result_html.txt
#test $1 
exit 0
