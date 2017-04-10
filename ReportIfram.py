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
      <h3>%s Load Test </h3>
        </div>
        <div style="padding:10px;">
          <h4> Test Des: %s<br>
               Test Time: %s </h4>
                <p>测试结果概述</p>
                  <div style="padding:20px;">
<p>

<table width="100%%" border="1" frame="box" rules="all" cellpadding="1" cellspacing="0" class="legendTable">
<tr class="legendRow">
%s
</table>
</p>
</div>
<p> 详细结果描述如下 </p>
<table>
<tr>
<tb>
%s
</tb>
</tr>
</table>
</body>
"""
def output_html(html_title, proxy_app_des, proxy_app_h4, dlist, htmlrp_des_list, fp):
    table_data_tr_td = get_table_data_tr_tdX(dlist) # table list 列表数据
    iframe_str = get_iframe_br(htmlrp_des_list)    #iframe 中详细的测试报告连接
    new_str = mod_app_html % (html_title, html_title, proxy_app_des, proxy_app_h4, table_data_tr_td, iframe_str)
    f =open(fp,"w")
    f.write(new_str)
    f.close()
    return fp

def output_data(source_data):
    table_data_tr_td = get_table_data_tr_tdX(source_data.destabledata) # table list 列表数据
    iframe_str = get_iframe_br(source_data.iframelist)    #iframe 中详细的测试报告连接
    new_str = mod_app_html % (source_data.title, source_data.title, source_data.des, source_data.testtime, table_data_tr_td, iframe_str)
    fp = "%s_%s.html" % (source_data.title, source_data.testtime)
    f =open(fp,"w")
    f.write(new_str)
    f.close()
    return fp

def get_iframe_br(htmlrp_des_list):
    """iframe 中详细的测试报告连接 """
    res = """<tb><iframe id="iframe" src="%s" height="700" width="850" frameborder="0" scrolling="no">%s</iframe></tb>\n"""
    com = ""
    id = 0
    for i in htmlrp_des_list:
        com_line = res % (str(i[1]), str(i[0])) #[0] html report title; [1] html report fp
        if 0 == id:
            com = "%s%s" % (com, com_line)
            id = id + 1
        else:
            com = "%s%s<br>" % (com, com_line)
            id = 0
            
    return com


def get_table_data_tr_tdX(dlist):
    """table list 列表数据 """
    com =""
    for i in dlist:
	com = "\n%s" % com
	for j in i:
	    com = "%s<td>%s</td>" % (com, j) 
	com = "%s<tr>" % com
        #com = "%s\n<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (com, i[0],i[1],i[2],i[3],i[4])
    return com

if __name__=="__main__":
    ifram_list=[["num_app_proxy", "1219_10_app_proxy.log_1482136270.41.html"],\
                ["proxy_test_use_", "proxy_test_use_time_app_proxy_1482144366.5.html"],\
                ["precent_app_proxy", "precent_app_proxy_1482143740.02.html"]]
    output_html(html_title="app proxy 测试报告", proxy_app_des="app proxy 测试报告", proxy_app_h4="2016-12-20", dlist=[[1,1,1]], htmlrp_des_list=ifram_list, fp="prox.html")
