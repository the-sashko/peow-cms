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
	os.makedirs('tmp/build/media/',0o777,1)
	os.makedirs('tmp/build/xml/',0o777,1)
	os.makedirs('tmp/build/xml/sitemap/',0o777,1)
	os.makedirs('tmp/build/xml/feed/',0o777,1)
	getParams()
	makeRobots()
	print('Building articles...')
	buildArticles()
	print('Building main page...')
	buildIndex()
	print('Building tags...')
	buildTags()
	print('Building topics...')
	buildTopics()
	print('Building static pages...')
	buildPages()
	buildErrPages()
	print('Building archives...')
	buildTimeline()
	print('Building assets...')
	generateAssets()
	print('Building xml data...')
	generateXML()

def makePage(template='index',content='',fileName=''):
	if(fileName==''):
		fileName=template
	params['templatepage']=open('content/html/'+template+'.html', 'r').read()
	params['content']=content
	if(len(params['path'])>0):
		params['title']=' / '.join(params['path'])+' / '+params['sitename']
	else:
		params['title']=params['sitename']+' – Головна'
	page = templator.Templator(params,open('content/html/layout/main.html', 'r').read())
	page.html=makeLinks(page.html)

	
	page.html=page.html.replace("\n",'')
	page.html=page.html.rstrip()
	page.html=re.sub(r'\s',' ',page.html,flags=re.U)
	page.html=re.sub(r' +',' ',page.html,flags=re.U)

	open('tmp/build'+fileName+'.html', 'w+').write(page.html)

def getParams():
	global params
	params=json.loads(open('config/main.json', 'r').read())
	params['main_menu']=json.loads(open('config/menu.json', 'r').read())
	#params['git']=json.loads(open('config/git.json', 'r').read())
	#params['ftp']=json.loads(open('config/ftp.json', 'r').read())
	params['tags']=json.loads(open('content/taxonomy/tags.json', 'r').read())
	params['topics']=json.loads(open('content/taxonomy/topics.json', 'r').read())
	params['langfull']=params['lang']
	params['lang']=re.sub(r'^(.*?)_.*?$',lambda data: data.group(1),params['langfull'],flags=re.U)
	params['yearstart']=re.sub(r'^(.*?)-(.*?)-(.*?)$',lambda data: data.group(1),params['sitecreatedate'],flags=re.U)
	params['path']=[]
	params['currenturl']=''
	params['meta-image']=params['protocol']+'://'+params['domain']+'/assets/img/logo.png'
	params['now']={
		'year':time.strftime("%Y"),
		'month':time.strftime("%m"),
		'day':time.strftime("%d")
	}
	return 1

def makeRobots():
	robotsText='User-agent: *'+"\n"
	robotsText=robotsText+'Allow: /'+"\n"
	robotsText=robotsText+'sitemap: '+params['protocol']+'://'+params['domain']+'/sitemap.xml'+"\n"
	robotsText=robotsText+'Host: '+params['domain']
	open('tmp/build/robots.txt', 'w+').write(robotsText)

def buildArticles():
	params['articles']={}
	params['index']=[]
	params['currenturl']=''
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

			metaDescription=params['meta-description']
			params['meta-description']=params['articles'][intdate]['summary']
			params['meta-description']=params['meta-description'].replace("\n",' ')
			params['meta-description']=re.sub(r'<(.*?)>','',params['meta-description'],flags=re.U|re.M)
			params['meta-description']=re.sub(r' $','',params['meta-description'],flags=re.U|re.M)
			params['currenturl']=params['protocol']+'://'+params['domain']+'/p/'+params['articles'][intdate]['uri']+'/'
			params['meta-image']=params['protocol']+'://'+params['domain']+'/media/'+params['articles'][intdate]['uri']+'/full.png'
			makePage('post',params['articles'][intdate],'/p/'+params['articles'][intdate]['uri'])
			params['meta-description']=metaDescription
	
	params['meta-image']=params['protocol']+'://'+params['domain']+'/assets/img/logo.png'
	params['index'].sort(reverse=True)

def buildPages():
	params['pages']={}
	params['currenturl']=''
	for page in os.listdir('content/pages'):
		if os.path.isdir('content/pages/'+page) and os.path.isfile('content/pages/'+page+'/content.md') and os.path.isfile('content/pages/'+page+'/data.json'):
			params['pages'][page]=json.loads(open('content/pages/'+page+'/data.json', 'r').read())
			params['pages'][page]['text']=markup.md2html(open('content/pages/'+page+'/content.md', 'r').read())
			try:
				params['pages'][page]['uri']
			except KeyError:
				params['pages'][page]['uri']=page
			params['path']=[params['pages'][page]['title']]
			params['currenturl']=params['protocol']+'://'+params['domain']+'/'+params['pages'][page]['uri']+'/'
			makePage('page',params['pages'][page],'/'+params['pages'][page]['uri'])

def buildErrPages():
	makePage('error','','/404')

def buildTags():
	# do it by map
	params['currentposts']=[]
	tags=params['tags']
	params['tags']=[]
	params['currenturl']=''
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
			params['path']=[tag['title'],'Теги']
			params['currenturl']=params['protocol']+'://'+params['domain']+'/tag/'+tag['name']+'/'
			makePage('list',params,'/tag/'+tag['name'])
	params['path']=['Всі мітки']
	params['currenturl']=params['protocol']+'://'+params['domain']+'/tag/all/'
	makePage('tags',params,'/tag/all')
	return 1

def buildTopics():
	# do it by map
	params['currentposts']=[]
	topics=params['topics']
	params['topics']=[]
	params['currenturl']=''
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
			params['path']=[topic['title'],'Теми']
			params['currenturl']=params['protocol']+'://'+params['domain']+'/topic/'+topic['name']+'/'
			params['meta-image']=params['protocol']+'://'+params['domain']+'/assets/img/topic/'+topic['name']+'.png'
			makePage('list',params,'/topic/'+topic['name'])
	params['path']=['Всі теми']
	params['currenturl']=params['protocol']+'://'+params['domain']+'/topic/all/'
	params['meta-image']=params['protocol']+'://'+params['domain']+'/assets/img/logo.png'
	makePage('topics',params,'/topic/all')
	return 1

def buildIndex():
	params['currentposts']=[]
	for key in params['index']:
		article=params['articles'][key]
		params['currentposts'].append(article)
	params['path']=[]
	params['currenturl']=params['protocol']+'://'+params['domain']+'/'
	makePage('list',params,'/index')
	return 1

def generateAssets():
	os.makedirs('tmp/build/assets/css/',0o777,1)
	shutil.copytree('content/assets/css/lib/','tmp/build/assets/css/lib/')
	#shutil.copy('content/assets/css/style.css','tmp/build/assets/css/style.min.css')
	os.makedirs('tmp/build/assets/js/',0o777,1)
	#shutil.copy('content/assets/js/app.js','tmp/build/assets/js/app.min.js')
	shutil.copytree('content/assets/img/','tmp/build/assets/img/')
	shutil.copytree('content/assets/fonts/','tmp/build/assets/fonts/')
	minify.css(params['assetsversion'])
	minify.js()
	return 1

def buildTimeline():
	return 1

def generateXML():
	mainSitemap='<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"\n"
	mainSitemap=mainSitemap+"\t"+'<sitemap>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/xml/sitemap/index.xml</loc>'+"\n\t\t"+'<lastmod>'+datetime.today().strftime("%Y-%m-%dT%H:%M:%S+00:00")+'</lastmod>'+"\n\t"+'</sitemap>'+"\n"
	mainSitemap=mainSitemap+"\t"+'<sitemap>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/xml/sitemap/pages.xml</loc>'+"\n\t\t"+'<lastmod>'+datetime.today().strftime("%Y-%m-%dT%H:%M:%S+00:00")+'</lastmod>'+"\n\t"+'</sitemap>'+"\n"
	mainSitemap=mainSitemap+"\t"+'<sitemap>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/xml/sitemap/posts.xml</loc>'+"\n\t\t"+'<lastmod>'+datetime.today().strftime("%Y-%m-%dT%H:%M:%S+00:00")+'</lastmod>'+"\n\t"+'</sitemap>'+"\n"
	mainSitemap=mainSitemap+"\t"+'<sitemap>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/xml/sitemap/tags.xml</loc>'+"\n\t\t"+'<lastmod>'+datetime.today().strftime("%Y-%m-%dT%H:%M:%S+00:00")+'</lastmod>'+"\n\t"+'</sitemap>'+"\n"
	mainSitemap=mainSitemap+"\t"+'<sitemap>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/xml/sitemap/topics.xml</loc>'+"\n\t\t"+'<lastmod>'+datetime.today().strftime("%Y-%m-%dT%H:%M:%S+00:00")+'</lastmod>'+"\n\t"+'</sitemap>'+"\n"
	mainSitemap=mainSitemap+'</sitemapindex>'
	open('tmp/build/sitemap.xml', 'w+').write(mainSitemap)
	indexSitemap='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"\n"
	indexSitemap=indexSitemap+"\t"+'<url>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/</loc>'+"\n\t\t"+'<changefreq>hourly</changefreq>'+"\n\t\t"+'<priority>0.6</priority>'+"\n\t"+'</url>'+"\n"
	indexSitemap=indexSitemap+'</urlset>'
	open('tmp/build/xml/sitemap/index.xml', 'w+').write(indexSitemap)
	pagesSitemap='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"\n"
	for page in os.listdir('content/pages'):
		if os.path.isfile('content/pages/'+page+'/data.json'):
			pageParams=json.loads(open('content/pages/'+page+'/data.json', 'r').read())
			pagesSitemap=pagesSitemap+"\t"+'<url>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/'+pageParams['uri']+'/</loc>'+"\n\t\t"+'<changefreq>monthly</changefreq>'+"\n\t\t"+'<priority>0.3</priority>'+"\n\t"+'</url>'+"\n"
	pagesSitemap=pagesSitemap+'</urlset>'
	open('tmp/build/xml/sitemap/pages.xml', 'w+').write(pagesSitemap)
	postsSitemap='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"\n"
	for article in os.listdir('content/articles'):
		if os.path.isfile('content/articles/'+article+'/data.json'):
			postParams=json.loads(open('content/articles/'+article+'/data.json', 'r').read())
			postsSitemap=postsSitemap+"\t"+'<url>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/p/'+postParams['uri']+'/</loc>'+"\n\t\t"+'<changefreq>daily</changefreq>'+"\n\t\t"+'<priority>0.9</priority>'+"\n\t"+'</url>'+"\n"
	postsSitemap=postsSitemap+'</urlset>'
	open('tmp/build/xml/sitemap/posts.xml', 'w+').write(postsSitemap)
	tagsSitemap='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"\n"
	for tag in params['tags']:
		tagsSitemap=tagsSitemap+"\t"+'<url>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/tag/'+tag['name']+'/</loc>'+"\n\t\t"+'<changefreq>hourly</changefreq>'+"\n\t\t"+'<priority>0.8</priority>'+"\n\t"+'</url>'+"\n"
	tagsSitemap=tagsSitemap+'</urlset>'
	open('tmp/build/xml/sitemap/tags.xml', 'w+').write(tagsSitemap)
	topicsSitemap='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"\n"
	for topic in params['topics']:
		topicsSitemap=topicsSitemap+"\t"+'<url>'+"\n\t\t"+'<loc>'+params['protocol']+'://'+params['domain']+'/topic/'+topic['name']+'/</loc>'+"\n\t\t"+'<changefreq>hourly</changefreq>'+"\n\t\t"+'<priority>0.8</priority>'+"\n\t"+'</url>'+"\n"
	topicsSitemap=topicsSitemap+'</urlset>'
	open('tmp/build/xml/sitemap/topics.xml', 'w+').write(topicsSitemap)

	rss='<rss xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">'+"\n"
	rss=rss+"\t"+'<channel>'+"\n"
	rss=rss+"\t\t"+'<description>'+"\n"
	rss=rss+"\t\t\t"+'<![CDATA[ ]]>'+"\n"
	rss=rss+"\t\t"+'</description>'+"\n"
	rss=rss+"\t\t"+'<title>'+params['sitename']+' RSS</title>'+"\n"
	rss=rss+"\t\t"+'<image>'+"\n"
	rss=rss+"\t\t\t"+'<url>'+params['protocol']+'://'+params['domain']+'/assets/img/logo.png</url>'+"\n"
	rss=rss+"\t\t\t"+'<title>'+params['sitename']+'</title>'+"\n"
	rss=rss+"\t\t\t"+'<link>'+params['protocol']+'://'+params['domain']+'</link>'+"\n"
	rss=rss+"\t\t"+'</image>'+"\n"
	rss=rss+"\t\t"+'<generator>PewCMS</generator>'+"\n"
	rss=rss+"\t\t"+'<link>'+params['protocol']+'://'+params['domain']+'/p/'+postParams['uri']+'/</link>'+"\n"
	for article in os.listdir('content/articles'):
		if os.path.isfile('content/articles/'+article+'/content.md') and os.path.isfile('content/articles/'+article+'/data.json'):
			postParams=json.loads(open('content/articles/'+article+'/data.json', 'r').read())
			rss=rss+"\t\t"+'<item>'+"\n"
			rss=rss+"\t\t\t"+'<title>'+postParams['title']+'</title>'+"\n"
			rss=rss+"\t\t\t"+'<description>'+"\n"
			rss=rss+"\t\t\t"+'<![CDATA['+"\n"

			rssText=''
			rssText=markup.md2html(markup.getSummary(open('content/articles/'+article+'/content.md', 'r').read()))
			if(len(rssText)<1):
				rssText=markup.md2html(open('content/articles/'+article+'/content.md', 'r').read())
			rssText=rssText.replace("\n",' ')
			rssText=re.sub(r'<(.*?)>','',rssText,flags=re.U|re.M)
			rssText=re.sub(r' $','',rssText,flags=re.U|re.M)
			rss=rss+"\t\t\t\t"+rssText+"\n"
			rss=rss+"\t\t\t"+']]>'+"\n"
			rss=rss+"\t\t\t"+'</description>'+"\n"
			rss=rss+"\t\t\t"+'<link>'+params['protocol']+'://'+params['domain']+'/p/'+postParams['uri']+'/</link>'+"\n"
			rss=rss+"\t\t\t"+'<guid>'+params['protocol']+'://'+params['domain']+'/p/'+postParams['uri']+'/</guid>'+"\n"
			rss=rss+"\t\t"+'</item>'+"\n"
	rss=rss+"\t"+'</channel>'+"\n"
	rss=rss+"\t"+'</rss>'+"\n"
	open('tmp/build/xml/feed/rss.xml', 'w+').write(rss)

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