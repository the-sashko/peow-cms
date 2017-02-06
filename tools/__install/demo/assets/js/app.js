window.onload = function() {
	document.getElementById('pda-menu-link').onclick =function(){
		var menu=document.getElementById('header-menu')
		if(menu.style.display=='none'||menu.style.display==''){
			var style = 'block';
		} else {
			var style = 'none';
		}
		menu.style.display=style;
	}	
	console.clear();
	console.log('%c Designed by Iskander Al-Slobojani', 'color: #880000; font-size:1.5em; font-weight:bold;');
	console.info('%c Write me to: feedback@mrakobis.com', 'color: #008800; font-size:1em; font-weight:bold;');
}