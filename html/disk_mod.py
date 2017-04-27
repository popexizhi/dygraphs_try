#-*-coding:utf8-*-
disk_str="""
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
<td class="header_page">disk: iostat -d -x </td>
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
                    </table>
<script type="text/javascript">
    var ip = "%s";
    var stat = "iostat";
    var dir = "%s";
    //stat + "/" + ip + "_" + stat + x[i]
    document.getElementById("ip").innerHTML = "ip :"+ ip;
    var x = [
    //"vmstat/192.168.1.212__vmstat/vmstat_memory-cache.csv",
    //"vmstat/192.168.1.212__vmstat/vmstat_cpu-us.csv"
    "iostat_rkB_s.csv",
    "iostat_svctm.csv",
    "iostat_wkB_s.csv",
    "iostat_avgqu-sz.csv",
    "iostat_await.csv",
    "iostat_util.csv"
        ];

    for (var i =0; i<=x.length; i++){
      var doc=dir + "/" + ip + "__" + stat + "/" + x[i];
      g2 = new Dygraph(
        document.getElementById("graphdivx"+i), //graphdivx1
        //x[i],
        doc,
        {
          rollPeriod: 1,
          //avoidMinZero: true,//y轴的最小值不为0，相当于y=0那条线上升了
          axisLabelWidth:100,//X Y轴的标题的宽度
          fillGraph: true,//背景色显示      
          //stackedGraph: true, //叠加图      
          //stepPlot: true, //数据显示增长步骤
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
                                 disk 统计
                                 <pre>
                                 rrqm/s:  每秒进行 merge 的读操作数目。即 rmerge/s
                                 wrqm/s:  每秒进行 merge 的写操作数目。即 wmerge/s
                                 r/s:  每秒完成的读 I/O 设备次数。即 rio/s
                                 w/s:  每秒完成的写 I/O 设备次数。即 wio/s
                                 rsec/s:  每秒读扇区数。即 rsect/s
                                 wsec/s:  每秒写扇区数。即 wsect/s
                                 rkB/s:  每秒读K字节数。是 rsect/s 的一半，因为每扇区大小为512字节。
                                 wkB/s:  每秒写K字节数。是 wsect/s 的一半。
                                 avgrq-sz:  平均每次设备I/O操作的数据大小 (扇区)。
                                 avgqu-sz:  平均I/O队列长度。
                                 await:  平均每次设备I/O操作的等待时间 (毫秒)。
                                 svctm: 平均每次设备I/O操作的服务时间 (毫秒)。
                                 %%util:  一秒中有百分之多少的时间用于 I/O 操作，即被io消耗的cpu百分比
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
