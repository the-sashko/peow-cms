import markdown2,re

def md2html(text):
	return postEditText(markdown2.markdown(prepareText(text)))

def prepareText(text):
	text=re.sub(r'\<\!\-\-.*?\-\-\>','', text,flags=re.M|re.U)
	text=text.replace('--','—')
	text=text.replace(' - ','—')
	text=text.replace('--','—')
	text=text.replace('’','"')
	text=text.replace('<<','"')
	text=text.replace('>>','"')
	text=text.replace('‘','"')
	text=text.replace('”','"')
	text=text.replace('“','"')
	text=text.replace('„','"')
	text=text.replace('«','"')
	text=text.replace('»','"')
	text=text.replace("''",'"')
	text=text.replace("'","’")
	text=re.sub(r'"+', '"', text,flags=re.M|re.U)
	text=re.sub(r'"(.*?)"', lambda data: '«'+data.group(1)+'»', text,flags=re.M|re.U)
	text=re.sub(r'\r', '\n', text,flags=re.M|re.U)
	text=re.sub(r'\n+', '\n', text,flags=re.M|re.U)
	text=re.sub(r'	+',' ',text,flags=re.M|re.U)
	text=re.sub(r'\.\.\.+','…',text,flags=re.M|re.U)
	text=re.sub(r' +',' ',text,flags=re.M|re.U)
	text=re.sub(r'\n ', '\n', text,flags=re.M|re.U)
	text=re.sub(r' \n', '\n', text,flags=re.M|re.U)
	text=re.sub(r'^ ','',text,flags=re.U)
	text=re.sub(r'^\n','',text,flags=re.U)
	text=re.sub(r'\n','\n\n',text,flags=re.M|re.U)
	return text

def postEditText(html):#«братьями»
	html=prepareText(html)
	html=re.sub(r'\n+', '\n', html,flags=re.M|re.U)
	html=re.sub(r'DEL(.*?)DEL', lambda data: '<strike>'+data.group(1)+'</strike>', html,flags=re.M|re.U)
	html=html.replace('[u]','<span class="underlined">')
	html=html.replace('[/u]','</span>')
	html=html.replace('<li> <p>','<li>')
	html=html.replace('<li><p>','<li>')
	html=html.replace('<li>\n<p>','<li>')
	html=html.replace('</p> </li>','</li>')
	html=html.replace('</p></li>','</li>')
	html=html.replace('</p>\n</li>','</li>')
	html=html.replace('<blockquote> </blockquote>','')
	html=html.replace('<blockquote></blockquote>','')
	html=html.replace('<blockquote>\n</blockquote>','')
	return html

def getSummary(text):
	return re.split(r'^\<\!\-\-cut\-\-\>.*?$', text,flags=re.M|re.U)[0]