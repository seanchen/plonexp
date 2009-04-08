<script src="http://www.google.com/jsapi" type="text/javascript"></script>
<script type="text/javascript">
  google.load("gdata", "1.x", { packages : ["blogger"] });
</script>
  <!-- Add-On Settings -->
  <script type="text/JavaScript">

    /*******  Menu 0 Add-On Settings *******/
    var b = qmad.qm1 = new Object();

    // Box Animation Add On
    b.box_animation_frames = 20;
    b.box_accelerator = 0.4;
    b.box_position = "center";

    // Item Bullets (CSS - Imageless) Add On
    b.ibcss_apply_to = "parent";
    b.ibcss_main_type = "arrow-head-v";
    b.ibcss_main_direction = "down";
    b.ibcss_main_size = 5;
    b.ibcss_main_bg_color = "transparent";
    b.ibcss_main_border_color = "#555555";
    b.ibcss_main_border_color_hover = "#dd3300";
    b.ibcss_main_position_x = -19;
    b.ibcss_main_position_y = -4;
    b.ibcss_main_align_x = "right";
    b.ibcss_main_align_y = "middle";
    b.ibcss_sub_type = "arrow-head-v";
    b.ibcss_sub_direction = "right";
    b.ibcss_sub_size = 5;
    b.ibcss_sub_bg_color = "transparent";
    b.ibcss_sub_border_color = "#555555";
    b.ibcss_sub_border_color_hover = "#dd3300";
    b.ibcss_sub_position_x = -16;
    b.ibcss_sub_align_x = "right";
    b.ibcss_sub_align_y = "middle";

  </script>
<script type="text/javascript">

function buildFixesList(wenjians) {
var rootUL = document.createElement("ul");rootUL.id = "qm1";rootUL.className = "qmmc";
var topLI = document.createElement("li");var topHref = document.createElement("a");topHref.className = "qmparent";topHref.setAttribute("href", "javascript:void(0)");topHref.appendChild(document.createTextNode("Select Your FTA Receiver ..."));topLI.appendChild(topHref);
var wenjiansUL = document.createElement("ul");
for (var i = 0; i < wenjians.length; i ++) {    var wenJians = wenjians[i].wjs;
    var wenjianLI = document.createElement("li");    var wenjianHref = document.createElement("a");    wenjianHref.setAttribute("href", "javascript:void(0)");    wenjianHref.appendChild(document.createTextNode(wenjians[i].bq));    wenjianLI.appendChild(wenjianHref);
    var wjsUL = document.createElement("ul");    for (var j = 0; j < wenJians.length; j ++) {        var wjLI = document.createElement("li");        var wjHref = document.createElement("a");        wjHref.setAttribute("href", "javascript:void(0);");        wjHref.wz = wenJians[j].wj;        wjHref.onclick = xianShiWenjian;        wjHref.appendChild(document.createTextNode(wenJians[j].bq));        wjLI.appendChild(wjHref);
        wjsUL.appendChild(wjLI);    }
    wenjianLI.appendChild(wjsUL);
    wenjiansUL.appendChild(wenjianLI);}
topLI.appendChild(wenjiansUL);
rootUL.appendChild(topLI);
var clearLI = document.createElement("li");clearLI.className = "qmclear";clearLI.appendChild(document.createTextNode("&nbsp;"));
rootUL.appendChild(clearLI);return rootUL;
}

function xianShiWenjian(event) {
if (!event) event = window.event; var theSource = event.target ? event.target : event.srcElement;window.location = theSource.wz;
}

function buildLatestFixes(wenjians) {
    var qm1 = buildFixesList(wenjians);var fixesDiv = document.getElementById("fixesDiv");fixesDiv.innerHTML='';fixesDiv.appendChild(qm1);qm_create(1,false,0,500,false,false,false,false,false);
}
</script>

<script type="text/javascript">
  function getWenjians(data) {
    // alert(data);
    var wenjians = []
    var brands = data.split('AAAA');
    for(i = 0; i < brands.length; i ++) {
      var brandStr = brands[i].split('BBBB');
      var brand = {};
      // brand name
      brand.bq = brandStr[0];
      brand.wjs = [];
      // brand's model list
      var models = brandStr[1].split('MMMM');
      for(j = 0; j < models.length; j ++) {
        var modelValue = models[j].split('UUUU');
        // model name
        var model = {};
        model.bq = modelValue[0];
        model.wj = modelValue[1];

        brand.wjs[j] = model;
      }

      //alert(brand.bq + "------" + brand.wjs);
      wenjians[i] = brand;
    }
    return wenjians;
  }

  function _run() {

    var content = document.getElementById('fixesDiv');
    
    var bloggerService =
        new google.gdata.blogger.BloggerService('openkeys');
    
    var feedUri = 'http://openkeys.blogspot.com/feeds/posts/default';

    var handleQueryResults = function(resultsFeedRoot) {

      var blogFeed = resultsFeedRoot.feed;

      var postEntries = blogFeed.getEntries();
      var postContent = postEntries[0].getContent().getText();
      
      buildLatestFixes(getWenjians(postContent));
    };
    
    var handleError = function(error) {
      content.innerHTML = theDate + 'Please Use <a href="#" onclick="document.forms[0].q.value=innerHTML; document.forms[0].submit();">Google Chrome</a> to download the latest fixes!';
    };
    
    var startDate = new Date('Feburary 09, 2008 08:00:00');
    var endDate = new Date('Feburary 10, 2008 06:00:00');
    
    var query = new google.gdata.blogger.BlogPostQuery(feedUri);
    query.setPublishedMin(new google.gdata.DateTime(startDate));
    query.setPublishedMax(new google.gdata.DateTime(endDate));
    
    bloggerService.getBlogPostFeed(query, handleQueryResults, handleError);
  }

  google.setOnLoadCallback(_run);
</script>

<table align="center"><tbody>
    <tr>
        <td valign="middle"><font size="2">Latest Fixes [<b><script type="text/javascript">document.write((new Date()).toDateString());</script></b>]: </font></td>
        <td valign="middle">
          <div id="fixesDiv">Loading...</div>
        </td>
    </tr>
</tbody></table>

<style type="text/css">
.qmmc .qmdivider{display:block;font-size:1px;border-width:0px;border-style:solid;position:relative;z-index:1;}.qmmc .qmdividery{float:left;width:0px;}.qmmc .qmtitle{display:block;cursor:default;white-space:nowrap;position:relative;z-index:1;}.qmclear {font-size:1px;height:0px;width:0px;clear:left;line-height:0px;display:block;float:none !important;}.qmmc {position:relative;zoom:1;z-index:10;}.qmmc a, .qmmc li {float:left;display:block;white-space:nowrap;position:relative;z-index:1;}.qmmc div a, .qmmc ul a, .qmmc ul li {float:none;}.qmsh div a {float:left;}.qmmc div{visibility:hidden;position:absolute;}.qmmc li {z-index:auto;}.qmmc ul {left:-10000px;position:absolute;z-index:10;}.qmmc, .qmmc ul {list-style:none;padding:0px;margin:0px;}.qmmc li a {float:none}.qmmc li:hover>ul{left:auto;}#qm1 ul {top:100%;}#qm1 ul li:hover>ul{top:0px;left:100%;}
  #qm1  
  { 
    width:auto;
    background-color:transparent;
  }
  #qm1 a  
  { 
    padding:5px 40px 5px 8px;
    background-color:#ffffff;
    color:#000000;
    font-family:Arial;
    font-size:11px;
    text-decoration:none;
    border-width:1px;
    border-style:solid;
    border-color:#dd3300;
  }
  #qm1 a:hover  
  { 
    background-color:#fcebcd;
  }
  #qm1 li:hover>a 
  { 
    background-color:#fcebcd;
  }
  body #qm1 .qmactive, body #qm1 .qmactive:hover  
  { 
    background-color:#f9d08c;
    text-decoration:underline;
  }
  #qm1 div, #qm1 ul 
  { 
    padding:5px;
    margin:-1px 0px 0px;
    background-color:#fcebcd;
    border-width:1px;
    border-style:solid;
    border-color:#dd3300;
  }
  #qm1 div a, #qm1 ul a 
  { 
    padding:2px 40px 2px 5px;
    background-color:transparent;
    border-width:0px;
    border-style:none;
    border-color:#000000;
  }
  #qm1 div a:hover  
  { 
    background-color:transparent;
    color:#dd3300;
    text-decoration:underline;
  }
  #qm1 ul li:hover>a  
  { 
    background-color:transparent;
    color:#dd3300;
    text-decoration:underline;
  }
  body #qm1 div .qmactive, body #qm1 div .qmactive:hover  
  { 
    background-color:transparent;
    color:#dd3300;
  }
  #qm1 .qmtitle 
  { 
    cursor:default;
    padding:3px 0px 3px 4px;
    color:#444444;
    font-family:arial;
    font-size:11px;
    font-weight:bold;
  }
  #qm1 .qmdividerx  
  { 
    border-top-width:1px;
    margin:4px 0px;
    border-color:#bfbfbf;
  }
  #qm1 .qmdividery  
  { 
    border-left-width:1px;
    height:15px;
    margin:4px 2px 0px;
    border-color:#aaaaaa;
  }
  ul#qm1 .qmparent  
  { 
    background-image:url(qmimages/cssalt1_arrow_down.gif);
    background-repeat:no-repeat;
    background-position:97% 50%;
  }
  ul#qm1 li:hover > a.qmparent  
  { 
    background-image:url(qmimages/cssalt1_arrow_down_hover.gif);
    text-decoration:underline;
  }
  ul#qm1 ul .qmparent 
  { 
    background-image:url(qmimages/cssalt1_arrow_right.gif);
  }
  ul#qm1 ul li:hover > a.qmparent 
  { 
    background-image:url(qmimages/cssalt1_arrow_right_hover.gif);
  }
.qmfv{visibility:visible !important;}.qmfh{visibility:hidden !important;}
</style>