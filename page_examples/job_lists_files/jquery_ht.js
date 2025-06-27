//edit by sammy 2013.9.5
$(document).ready(function(){
//20130131 topmenu
$("#jq_topmenu li").hover(function(){$(this).addClass("hover").find("div.jq_hidebox").show();},function(){$(this).removeClass("hover").find("div.jq_hidebox").hide();});

$("#zx_topmenu li").hover(function(){$(this).addClass("hover").find("div.zx_hidebox").show();},function(){$(this).removeClass("hover").find("div.zx_hidebox").hide();});
//左侧弹出
$('#jq_menuArea li.hover').hover(function(){$(this).addClass('corrent').find('div').show();},function(){$(this).removeClass('corrent').find('div').hide();});
$("#jq_menuArea").delegate(".jq_close","click",function(){$("#jq_menuArea div.boxHide").hide();});
/*$('#jq_menuArea li#a1').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b1');});
$('#jq_menuArea li#a3').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b3');});
$('#jq_menuArea li#a5').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b5');});
$('#jq_menuArea li#a6').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b6');});
$('#jq_menuArea li#a7').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b7');});
$('#jq_menuArea li#a8').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b8');});
$('#jq_menuArea li#a9').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b9');});
$('#jq_menuArea li#a11').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b11');});
$('#jq_menuArea li#a12').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b12');});
$('#jq_menuArea li#a13').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b13');});
$('#jq_menuArea li#a14').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b14');});
$('#jq_menuArea li#a15').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b15');});
$('#jq_menuArea li#a16').hover(function(){$(this).find('div').load('themes/htBook/shoudong/menuArea_sd.html #b16');});*/

$("#hoverLesson").hover(function(){$("#jq_menuArea").fadeIn()},function(){$("#jq_menuArea").hide();});
if ($.browser.msie && ($.browser.version == "6.0") && !$.support.style) { 
$("#hoverLesson").hover(function(){$("select").hide()},function(){$("select").show()});
} 
//over
}); 
function addCookie(){
if(document.all){window.external.addFavorite('http://www.yinhangzhaopin.com', '银行招聘网');}
else if(window.sidebar){window.sidebar.addPanel('银行招聘网','http://www.yinhangzhaopin.com', "");}
else{alert("该操作被浏览器拒绝，请手动CTRL+D 添加");}
}
//function setHomepage(){if(document.all){document.body.style.behavior = 'url(#default#homepage)';document.body.setHomePage('http://v.htexam.com');}else if (window.sidebar){if(window.netscape){try{netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");}catch (e) {alert("该操作被浏览器拒绝，请手动添加");}}var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components.interfaces.nsIPrefBranch);prefs.setCharPref('browser.startup.homepage','http://v.htexam.com');}}