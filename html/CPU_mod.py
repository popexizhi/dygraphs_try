#-*-coding:utf8-*-
CPU_str="""
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
<td class="header_page">CPU: mpstat -P ALL </td>
<div id="ip"> </div>
						</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td class="sp_10px_row"></td>
			</tr>
			<tr>
				<td>
					<table width="100%%" border="0" cellspacing="0" cellpadding="0">
						<tr>
							<td>
								<table class="TableSummary" summary="Graph Summary Table">
								</table>
							</td>
							<td align="right" valign="top" width="180">
								<table border="0" cellspacing="0" cellpadding="0">
									<tr>
									</tr>
								</table>
							</td>
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
    var stat = "mpstat";
    var dir = "%s";
    //stat + "/" + ip + "_" + stat + x[i]
    document.getElementById("ip").innerHTML = "ip :"+ ip;
    var x = [
    "mpstat_sys.csv",
    "mpstat_usr.csv",
    "mpstat_iowait.csv",
    "mpstat_idle.csv",
    "mpstat_irq.csv",
    "mpstat_soft.csv"

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
          //fillGraph: true,//背景色显示      
          stackedGraph: true, //叠加图      
          stepPlot: true, //数据显示增长步骤
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
                                 CPU 使用监控:mpstat -P ALL 
                                 <pre>
        %%user      在internal时间段里，用户态的CPU时间(%%)，不包含nice值为负进程  (usr/total)*100
        %%nice      在internal时间段里，nice值为负进程的CPU时间(%%)   (nice/total)*100
        %%sys       在internal时间段里，内核时间(%%)       (system/total)*100
        %%iowait    在internal时间段里，硬盘IO等待时间(%%) (iowait/total)*100
        %%irq       在internal时间段里，硬中断时间(%%)     (irq/total)*100
        %%soft      在internal时间段里，软中断时间(%%)     (softirq/total)*100
        %%idle      在internal时间段里，CPU除去等待磁盘IO操作外的因为任何原因而空闲的时间闲置时间(%%) (idle/total)*100
        
        total_cur=user+system+nice+idle+iowait+irq+softirq
        total_pre=pre_user+ pre_system+ pre_nice+ pre_idle+ pre_iowait+ pre_irq+ pre_softirq
        user=user_cur – user_pre
        total=total_cur-total_pre
        其中_cur 表示当前值，_pre表示interval时间前的值。上表中的所有值可取到两位小数点
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
