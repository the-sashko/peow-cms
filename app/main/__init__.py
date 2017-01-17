import re,os,json,shutil,time
from transliterate import translit,get_available_language_codes
from datetime import datetime
from app import templator,markup,minify,media

params={}

def init():
	os.makedirs('tmp/build/topic/',0o777,1)
	os.makedirs('tmp/build/tag/',0o777,1)
	os.makedirs('tmp/build/p/',0o777,1)
	os.makedirs('tmp/build/media/',0o777,1)
	getParams()
	buildArticles()
	buildIndex()
	buildTags()
	buildTopics()
	buildPages()
	buildTimeline()
	generateAssets()
	generateXML()

def makePage(template='index',content='',fileName=''):
	if(fileName==''):
		fileName=template
	params['templatepage']=open('content/html/'+template+'.html', 'r').read()
	params['content']=content
	if(len(params['path'])>0):
		params['title']=' | '.join(params['path'])+' | '+params['sitename']
	else:
		params['title']=params['sitename']
	page = templator.Templator(params,open('content/html/layout/main.html', 'r').read())
	page.html=makeLinks(page.html)
	open('tmp/build'+fileName+'.html', 'w+').write(page.html)

def getParams():
	global params
	params=json.loads(open('config/main.json', 'r').read())
	params['main_menu']=json.loads(open('config/menu.json', 'r').read())
	#params['git']=json.loads(open('config/git.json', 'r').read())
	#params['ftp']=json.loads(open('config/ftp.json', 'r').read())
	params['tags']=json.loads(open('content/taxonomy/tags.json', 'r').read())
	params['topics']=json.loads(open('content/taxonomy/topics.json', 'r').read())
	params['yearstart']=re.sub(r'^(.*?)-(.*?)-(.*?)$',lambda data: data.group(1),params['sitecreatedate'],flags=re.U)
	params['path']=[]
	params['now']={
		'year':time.strftime("%Y"),
		'month':time.strftime("%m"),
		'day':time.strftime("%d")
	}
	return 1

def buildArticles():
	params['articles']={}
	params['index']=[]
	for article in os.listdir('content/articles'):
		if os.path.isdir('content/articles/'+article) and os.path.isfile('content/articles/'+article+'/content.md') and os.path.isfile('content/articles/'+article+'/data.json') and os.path.isdir('content/articles/'+article+'/media'):
			params['articles'][article]=json.loads(open('content/articles/'+article+'/data.json', 'r').read())
			try:
				params['articles'][article]['uri']
			except KeyError:
				params['articles'][article]['uri']=makeURI(params['articles'][article]['title'])
				open('content/articles/'+article+'/data.json', 'w+').write(json.dumps(params['articles'][article], sort_keys=True, indent=4))
			try:
				params['articles'][article]['date']
			except KeyError:
				params['articles'][article]['date']=datetime.today().strftime("%d.%m.%Y %H:%M:%S")
				open('content/articles/'+article+'/data.json', 'w+').write(json.dumps(params['articles'][article], sort_keys=True, indent=4))
			params['articles'][article]['text']=open('content/articles/'+article+'/content.md', 'r').read()
			params['articles'][article]['summary']=markup.md2html(markup.getSummary(params['articles'][article]['text']))
			params['articles'][article]['text']=markup.md2html(params['articles'][article]['text'])
			if(len(params['articles'][article]['summary'])<1):
				params['articles'][article]['summary']=params['articles'][article]['text']
			try:
				params['articles'][article]['tags']=[]
				for tagName in params['articles'][article]['taxonomy']['tags']:
					for tag in params['tags']:
						if(tagName==tag['name']):
							params['articles'][article]['tags'].append(tag)
			except KeyError:
				params['articles'][article]['taxonomy']['tags']=[]
				params['articles'][article]['tags']=[]

			try:
				params['articles'][article]['topics']=[]
				for tagName in params['articles'][article]['taxonomy']['topics']:
					for topic in params['topics']:
						if(tagName==topic['name']):
							params['articles'][article]['topics'].append(topic)
			except KeyError:
				params['articles'][article]['taxonomy']['topics']=[]
				params['articles'][article]['topics']=[]			

			params['articles'][article]['altdate'] = re.sub(r'^(.*?)\.(.*?)\.(.*?) (.*?)\:(.*?)\:(.*?)$',
				lambda data: data.group(3)+'-'+data.group(2)+'-'+data.group(1)+'T'+data.group(4)+':'+data.group(5),
				params['articles'][article]['date'],flags=re.U)
			intdate = int(re.sub(r'^(.*?)\.(.*?)\.(.*?) (.*?)\:(.*?)\:(.*?)$',
				lambda data: data.group(3)+data.group(2)+data.group(1)+data.group(4)+data.group(5)+data.group(6),
				params['articles'][article]['date'],flags=re.U))
			params['articles'][article]['date'] = re.sub(r'^(.*?)\.(.*?)\.(.*?) (.*?)\:(.*?)\:(.*?)$',
				lambda data: data.group(1)+'.'+data.group(2)+'.'+data.group(3)+' '+data.group(4)+':'+data.group(5),
				params['articles'][article]['date'],flags=re.U)

			media.generateMedia(article,params['articles'][article]['uri'])

			params['path']=[params['articles'][article]['title']]

			params['articles'][intdate]=params['articles'][article]
			params['index'].append(intdate)

			del params['articles'][article]

			makePage('post',params['articles'][intdate],'/p/'+params['articles'][intdate]['uri'])
	
	params['index'].sort(reverse=True)

def buildPages():
	params['pages']={}
	for page in os.listdir('content/pages'):
		if os.path.isdir('content/pages/'+page) and os.path.isfile('content/pages/'+page+'/content.md') and os.path.isfile('content/pages/'+page+'/data.json') and os.path.isdir('content/pages/'+page+'/media'):
			params['pages'][page]=json.loads(open('content/pages/'+page+'/data.json', 'r').read())
			params['pages'][page]['text']=markup.md2html(open('content/pages/'+page+'/content.md', 'r').read())
			try:
				params['pages'][page]['uri']
			except KeyError:
				params['pages'][page]['uri']=page
			params['path']=[params['pages'][page]['title'],'Теги']
			makePage('page',params['pages'][page],'/'+params['pages'][page]['uri'])

def buildTags():
	# do it by map
	params['currentposts']=[]
	tags=params['tags']
	params['tags']=[]
	for tag in tags:
		tagArticles=[]
		for key in params['index']:
			article=params['articles'][key]
			if(tag['name'] in article['taxonomy']['tags']):
				tagArticles.append(article)
		if len(tagArticles)>0:
			tag['count']=len(tagArticles)
			tag['size']=(10+int(tag['count']))/10
			params['tags'].append(tag)
			params['currentposts']=tagArticles
			params['path']=[tag['title'],'Мітка']
			makePage('list',params,'/tag/'+tag['name'])
	params['path']=['Всі мітки']
	makePage('tags',params,'/tag/all')
	return 1

def buildTopics():
	# do it by map
	params['currentposts']=[]
	topics=params['topics']
	params['topics']=[]
	for topic in topics:
		topicArticles=[]
		for key in params['index']:
			article=params['articles'][key]
			if(topic['name'] in article['taxonomy']['topics']):
				topicArticles.append(article)
		if len(topicArticles)>0:
			topic['count']=len(topicArticles)
			params['topics'].append(topic)
			params['currentposts']=topicArticles
			params['path']=[topic['title'],'Тема']
			makePage('list',params,'/topic/'+topic['name'])
	params['path']=['Всі теми']
	makePage('topics',params,'/topic/all')
	return 1

def buildIndex():
	params['currentposts']=[]
	for key in params['index']:
		article=params['articles'][key]
		params['currentposts'].append(article)
	params['path']=[]
	makePage('list',params,'/index')
	return 1

def generateAssets():
	os.makedirs('tmp/build/assets/css/',0o777,1)
	shutil.copy('content/assets/css/style.css','tmp/build/assets/css/style.min.css')
	minify.css()
	return 1

def buildTimeline():
	return 1

def generateXML():
	return 1

def makeURI(title):
	title=title.lower()
	if 'uk' in get_available_language_codes():
		title.replace('ё','йо')
		title.replace('э','е')
		title.replace('і','и')
		uri=translit(title,'uk',reversed=True)
	else:
		title.replace('є','е')
		title.replace('ї','и')
		title.replace('ъ','')
		uri=translit(title,'ru',reversed=True)
	uri=re.sub(r'[^a-z]','-',uri,flags=re.U)
	uri=re.sub(r'-+','-',uri,flags=re.U)
	return uri

def makeLinks(html):
	return html