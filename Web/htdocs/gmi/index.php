<?
include_once("common_includes.php");

$DEFPANELS = array();
$DEFPANELS[]=array('panel_title'=>'grandstream_left','panel_websections'=>'_grandstream_left','panel_type'=>'gxv3175_left','panel_content'=>'*')+$PANELDEFAULTS;
$DEFPANELS[]=array('panel_title'=>'grandstream_center','panel_websections'=>'_grandstream_center','panel_type'=>'gxv3175_center','panel_content'=>'*')+$PANELDEFAULTS;
$DEFPANELS[]=array('panel_title'=>'grandstream_right','panel_websections'=>'_grandstream_right','panel_type'=>'gxv3175_right','panel_content'=>'*')+$PANELDEFAULTS;

$panels=DB::query("SELECT * FROM user_gui_panels WHERE user='$_DOMOTIKA[username]' AND page='gmi' ORDER by panel_position,id");
if(!$panels or count($panels)<1) {
   $panels=$DEFPANELS;
   foreach($panels as $p) {
      $q="INSERT INTO user_gui_panels 
         (user,page,panel_title,panel_type,panel_cols,panel_height,panel_visible,panel_position,panel_sections,panel_websections,panel_selector,panel_content)
         VALUES
         ('".$_DOMOTIKA['username']."','gmi','".$p['panel_title']."','".$p['panel_type']."',
            '".$p['panel_cols']."','".$p['panel_height']."','".$p['panel_visible']."','".$p['panel_position']."',
            '".$p['panel_sections']."','".$p['panel_websections']."','".$p['panel_selector']."','".$p['panel_content']."')";
      DB::query($q);
   }

}
foreach($panels as $panel) {
      switch($panel['panel_type'])
      {
         case 'gxv3175_left':
            $buttonar_left=getPanelButtons($_DOMOTIKA['username'], $panel['panel_content'], $panel['panel_sections'], $panel['panel_websections'], $panel['panel_selector'],true,7);
            break;
         case 'gxv3175_center':
            $buttonar_center=getPanelButtons($_DOMOTIKA['username'], $panel['panel_content'], $panel['panel_sections'], $panel['panel_websections'], $panel['panel_selector'],true,7);
            break;
         case 'gxv3175_right':
            $buttonar_right=getPanelButtons($_DOMOTIKA['username'], $panel['panel_content'], $panel['panel_sections'], $panel['panel_websections'], $panel['panel_selector'],true,7);
            break;
      }
}

//$buttonar_left=getPanelButtons($_DOMOTIKA['username'], "*","*","_grandstream_left", "dmdomain","true",7);
//$buttonar_right=getPanelButtons($_DOMOTIKA['username'], "*","*","_grandstream_right", "dmdomain","true",7);
?>
<html>
<head>
<title>Domotika GMI Interface</title>
<link rel="stylesheet" href="/resources/pure/pure-nr-min.css">
<link rel="stylesheet" href="/resources/fontawesome/css/font-awesome.min.css">
<link href='style.css' type='text/css' rel='stylesheet'>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<!--
<script src="/resources/js/sockjs-0.3.min.js" ></script>
<script src="/resources/js/ajaxsocket.js" ></script>
-->
<script src="/resources/js/jquery-1.9.0.min.js"></script>
<script src="/resources/EventSource/eventsource.js"></script>
<script language="javascript" src="simpleGMI.js"></script>
<script type="text/javascript">
simpleGMI.fullScreen();
function sarca(data)
{
   alert(data);
}
setInterval(function(){
   simpleGMI.post('http://q.unixmedia.net/domotika/gmi/style.css', 'aaa=sarca', sarca);
}, 5000);
</script>
</head>
<body>
<div class="pure-g" >
   <div class="pure-u-1-3" style="padding-left:1.3333%;">
      <?
         foreach($buttonar_left as $but) {
      ?> 
         <div style="padding:5px;">
            <button class="pure-button pure-button-primary" style="width:100%;height:50px;" onclick="simpleGMI.refresh()"><?=$but['button_name']?></button>
         </div>
      <?
         }
      ?>
   </div>
   <div class="pure-u-1-3" style="width:31%">
      <div style="padding:5px;">
         <button class="pure-button pure-button-primary" style="width:100%;height:130px;" onclick="simpleGMI.refresh()">test</button>
      </div>
      <div style="height:80px" onclick="simpleGMI.refresh()">
      </div>
      <div style="padding:5px;display:none">
         <img src="https://192.168.4.45/enu/camera320x240.jpg" style="width:100%;height:190px" onclick="simpleGMI.refresh()"></img>
      </div>
      <div style="padding:5px;">
         <div class="pure-g">
            <div class="pure-u-1-3" >
               <button class="pure-button"><h1>15</h1></button>
            </div>
            <div class="pure-u-1-3" style="width:28%">
               <button class="pure-button"><h1>:</h1></button>
            </div>
            <div class="pure-u-1-3" >
               <button class="pure-button"><h1>15</h1></button>
            </div>
         </div>
      </div>   


   </div>
   <div class="pure-u-1-3" >
      <?
         foreach($buttonar_right as $but) {
      ?>
         <div style="padding:5px;">
            <button class="pure-button pure-button-primary" style="width:100%;height:50px;" onclick="simpleGMI.refresh()"><?=$but['button_name']?></button>
         </div>
      <?
         }
      ?>
   </div>

</div>

<div class="footer-bar">
<button onClick="simpleGMI.dial(0, 0, 0, 281, '', 1)" class="pure-button pure-button-secondary">
   <i class="fa fa-microphone fa-2x blackiconcolor"></i>
</button>
<span> STATUS: DEFAULT</span>
<button onClick="simpleGMI.refresh()" class="pure-button pure-button-secondary" style="float:right">
   <i class="fa fa-refresh fa-2x fa-spin blackiconcolor"></i>
</button>

</div>
<script>
var es = new EventSource("/sse");

var syncReceived = function(event) {
   var res=$.parseJSON(event.data);
   $.each(res.data.statuses, function(idx, val){
      // alert(val[3]);
   });
}
es.addEventListener("sync", syncReceived);
</script>
</body>
</html>
