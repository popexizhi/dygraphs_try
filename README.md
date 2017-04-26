# dygraphs_try
#要求监控主机安装sshpass，
#被监控主机安装sysstat
web版主机监控使用

#获得监控原始数据
sshdoing.sh ${dir} #${dir}为结果存放文件夹

#过滤原始数据生成csv文件
./stat.split.sh:test_all

