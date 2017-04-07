#-*-coding:utf8-*-
#构建html的总括报告使用eg:app proxy
mod_app_html="""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>%s</title>
<head>
<style type="text/css">
pre {
   background-color: gray; padding: 20px; border-bottom:1px;
}
</style>
</head>
</head>

<body style="font-family: Arial, Helvetica, sans-serif;
    font-family: "微软雅黑";">
    <div style=" box-shadow:0px 4px 4px rgba(0,0,0,0.12); padding:10px;">
      <h3>App Proxy Load Test </h3>
        <h4 style="color:#666">http://192.168.1.25:80/</h4>
        </div>
        <div style="padding:10px;">
          <h4> proxy_app_des: %s<br>
              %s </h4>
                <p>app proxy 测试结果概述</p>
                  <div style="padding:20px;">
<p>

<table width="100%%" border="1" frame="box" rules="all" cellpadding="1" cellspacing="0" class="legendTable">
<tr class="legendHeader">
<td>
Scale
</td>
<td>
Measurement
</td>
<td>
Graph Minimum
</td>
<td>
Graph Average
</td>
<td>
Graph Maximum
</td>
</tr>
<tr class="legendRow">
%s
</table>
</p>
</div>
<p> 详细结果描述如下 </p>
<table>
<tr>
<tb>
</pre>
</tb>
</tr>
</table>
%s
<pre>
ab res:
Requests per second: 113.01 /sec (mean)
Time per request: 88.484 [ms] (mean)
Time per request: 8.848 [ms] (mean, across all concurrent requests)
Transfer rate: 183.32 [Kbytes/sec] received
Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 33 88.0 2 295
Processing: 0 49 93.9 9 485
Waiting: 0 45 83.6 9 485
Total: 1 82 166.7 11 780
</pre>
</body>
"""
def output_html(html_title, proxy_app_des, proxy_app_h4, dlist, htmlrp_des_list, fp):
    table_data_tr_td = get_table_data_tr_td(dlist) # table list 列表数据
    iframe_str = get_iframe_br(htmlrp_des_list)    #iframe 中详细的测试报告连接
    new_str = mod_app_html % (html_title, proxy_app_des, proxy_app_h4, table_data_tr_td, iframe_str)
    f =open(fp,"w")
    f.write(new_str)
    f.close()
    return fp

def get_iframe_br(htmlrp_des_list):
    """iframe 中详细的测试报告连接 """
    res = """<iframe id="iframe" src="%s" height="700" width="1800" frameborder="0" scrolling="no">%s</iframe><br>\n"""
    com = ""
    for i in htmlrp_des_list:
        com_line = res % (str(i[1]), str(i[0])) #[0] html report title; [1] html report fp
        com = "%s%s" % (com, com_line)
    return com

def get_table_data_tr_td(dlist):
    """table list 列表数据 """
    com =""
    for i in dlist:
        com = "%s\n<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (com, i[0],i[1],i[2],i[3],i[4])
    return com

if __name__=="__main__":
    ifram_list=[["num_app_proxy", "1219_10_app_proxy.log_1482136270.41.html"],\
                ["proxy_test_use_", "proxy_test_use_time_app_proxy_1482144366.5.html"],\
                ["precent_app_proxy", "precent_app_proxy_1482143740.02.html"]]
    output_html(html_title="app proxy 测试报告", proxy_app_des="app proxy 测试报告", proxy_app_h4="2016-12-20", dlist=[[1,1,1,1,1,1]], htmlrp_des_list=ifram_list, fp="prox.html")
