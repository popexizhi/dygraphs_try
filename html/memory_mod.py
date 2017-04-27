#-*-coding:utf8-*-
memory_str="""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

<html>

	<head>
		<meta http-equiv="content-type" content="text/html;charset=UTF-8">
		<title></title>
		<link href="css_js/Properties.css" rel="stylesheet" media="screen">
        <script type="text/javascript" src="css_js/dygraph-combined-dev.js"></script>
	</head> 
	<body class="main">
		<table width="100%%" border="0" cellspacing="0" cellpadding="0">
			<tr>
				<td class="sp_10px_row"></td>
			</tr>
			<tr>
				<td>
					<table cols="2" width="100%%" height="20" border="0" cellpadding="0" cellspacing="0">
						<tr>
<td class="header_page">memory: vmstat </td>
<div id="ip"> </div>
						</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td class="sp_10px_row"></td>
			</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td class="sp_10px_row"></td>
			</tr>
			<tr>
				<td>
					<div class="pane_full">
                    <table>
                    <tr>
                    <td><div id="graphdivx0" style="width:700px; height:600px;"></div></td>
                    <td><div id="graphdivx1" style="width:700px; height:600px;"></div></td>
                    </tr>
                    <tr>
                    <td><div id="graphdivx2" style="width:700px; height:600px;"></div></td>
                    <td><div id="graphdivx3" style="width:700px; height:600px;"></div></td>
                    </tr>
                    <tr>
                    <td><div id="graphdivx4" style="width:700px; height:600px;"></div></td>
                    <td><div id="graphdivx5" style="width:700px; height:600px;"></div></td>
                    </tr>
                    <tr>
                    <td><div id="graphdivx6" style="width:700px; height:600px;"></div></td>
                    <td><div id="graphdivx7" style="width:700px; height:600px;"></div></td>
                    </tr>
                    </table>
<script type="text/javascript">
    var ip = "%s";
    var stat = "vmstat";
    var dir = "%s";
    //stat + "/" + ip + "_" + stat + x[i]
    document.getElementById("ip").innerHTML = "ip :"+ ip;
    var x = [
    "vmstat_memory-free.csv",
    "vmstat_memory-buff.csv",
    "vmstat_memory-cache.csv",
    "vmstat_memory-swpd.csv",
    "vmstat_swap-si.csv",
    "vmstat_swap-so.csv",
    "vmstat_io-bi.csv",
    "vmstat_io-bo.csv"

        ];

    for (var i =0; i<=x.length; i++){
      var doc=dir + "/" + ip + "__" + stat + "/" + x[i];
      g2 = new Dygraph(
        document.getElementById("graphdivx"+i), //graphdivx1
        //x[i],
        doc,
        {
          rollPeriod: 1,
          avoidMinZero: true,//y轴的最小值不为0，相当于y=0那条线上升了
          axisLabelWidth:100,//X Y轴的标题的宽度
          fillGraph: true,//背景色显示      
          //stackedGraph: true, //叠加图      
          stepPlot: true, //数据显示增长步骤
          maxNumberWidth:9, //整数位数超过这个值就转为科学计数法显示 1e6
          title:x[i],//
        }          // options
  );
  }//for end
</script>
                                    </div>
				</td>
			</tr>
			<tr>
				<td class="sp_10px_row"></td>
			</tr>
			<tr>
				<td>
				</td>
			</tr>
			<tr>
				<td class="sp_10px_row"></td>
			</tr>
			<tr>
				<td class="sp_5px_row"></td>
			</tr>
			<tr>
				<td class="sp_h_line"><img src="dot_trans.gif" alt="" height="1" width="1" border="0"></td>
			</tr>
			<tr>
				<td class="sp_5px_row"></td>
			</tr>
			<tr>
				<td>
					<div class="pane_full">
						<table width="100%%" border="0" cellspacing="0" cellpadding="0">
							<tr>
								<td valign="top"><font class="VerBl8"><b>Description: </b></font><font class="VerBl8">
                                 memory 统计
                                 <pre>
                                 1）procs
                                 a.r列表示运行和等待CPU时间片的进程数，这个值如果长期大于系统CPU个数，就说明CPU资源不足，可以考虑增加CPU；
                                 b.b列表示在等待资源的进程数，比如正在等待I/O或者内存交换等。
                                 2）memory
                                 a.swpd列表示切换到内存交换区的内存数量（以KB为单位）。如果swpd的值不为0或者比较大，而且si、so的值长期为0，那么这种情况一般不用担心，不会影响系统性能；
                                 b.free列表示当前空闲的物理内存数量（以KB为单位）；
                                 c.buff列表示buffers cache的内存数量，一般对块设备的读写才需要缓冲；
                                 d.cache列表示page cached的内存数量，一般作文件系统的cached，频繁访问的文件都会被cached。如果cached值较大，就说明cached文件数较多。如果此时IO中的bi比较小，就说明文件系统效率比较好。
                                 3）swap
                                 a.si列表示由磁盘调入内存，也就是内存进入内存交换区的数量；
                                 b.so列表示由内存调入磁盘，也就是内存交换区进入内存的数量
                                 c.一般情况下，si、so的值都为0，如果si、so的值长期不为0，则表示系统内存不足，需要考虑是否增加系统内存。
                                 4）IO
                                 a.bi列表示从块设备读入的数据总量（即读磁盘，单位KB/秒）
                                 b.bo列表示写入到块设备的数据总量（即写磁盘，单位KB/秒）
                                 这里设置的bi+bo参考值为1000，如果超过1000，而且wa值比较大，则表示系统磁盘IO性能瓶颈。
                                 5）system
                                 a.in列表示在某一时间间隔中观察到的每秒设备中断数；
                                 b.cs列表示每秒产生的上下文切换次数。
                                 上面这两个值越大，会看到内核消耗的CPU时间就越多。
                                 6）CPU
                                 a.us列显示了用户进程消耗CPU的时间百分比。us的值比较高时，说明用户进程消耗的CPU时间多，如果长期大于50%%，需要考虑优化程序啥的。
                                 b.sy列显示了内核进程消耗CPU的时间百分比。sy的值比较高时，就说明内核消耗的CPU时间多；如果us+sy超过80%%，就说明CPU的资源存在不足。
                                 c.id列显示了CPU处在空闲状态的时间百分比；
                                 d.wa列表示IO等待所占的CPU时间百分比。wa值越高，说明IO等待越严重。如果wa值超过20%%，说明IO等待严重。
                                 e.st列一般不关注，虚拟机占用的时间百分比。
                                 </pre>
                                <br>
									</font></td>
							</tr>
			<tr>
				<td class="sp_5px_row"></td>
			</tr>
						</table>
					</div>
				</td>
			</tr>
			<tr>
				<td></td>
			</tr>
			<tr>
				<td></td>
			</tr>
		</table>
	</body>
</html>
"""
