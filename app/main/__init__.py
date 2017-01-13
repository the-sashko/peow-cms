import os,json,shutil
from app import templator

params={}

def init():
	os.makedirs('tmp/build/html/',0o777,1)
	getParams()
	makePage('list')
	buildArticles()
	buildTags()
	buildTopics()
	buildPages()
	generateMedia()
	generateAssets()
	generateXML()

def makePage(template='index',content='',fileName='',path='/'):
	if(fileName==''):
		fileName=template
	params['templatepage']=open('html/'+template+'.html', 'r').read()
	params['content']=content
	print('--------------')
	print(content)
	page = templator.Templator(params,open('html/layout/main.html', 'r').read())
	open('tmp/build'+path+fileName+'.html', 'w+').write(page.html)

def getParams():
	global params
	params=json.loads(open('config/main.json', 'r').read())
	params['tags']=json.loads(open('taxonomy/tags.json', 'r').read())
	params['topics']=json.loads(open('taxonomy/topics.json', 'r').read())
	print(params)
	return 1

def buildArticles():
	params['articles']={}
	for article in os.listdir('articles'):
		if os.path.isdir('articles/'+article) and os.path.isfile('articles/'+article+'/content.md') and os.path.isfile('articles/'+article+'/data.json') and os.path.isdir('articles/'+article+'/media'):
			params['articles'][article]=json.loads(open('articles/'+article+'/data.json', 'r').read())
			params['articles'][article]['text']=open('articles/'+article+'/content.md', 'r').read()
			#print(os.listdir('articles/'+article))
			try:
				params['articles'][article]['uri']
			except KeyError:
				params['articles'][article]['uri']=article
			try:
				params['articles'][article]['date']
			except KeyError:
				params['articles'][article]['date']='00.00.000 00:00:00'
			print(params['articles'][article])
			makePage('post',params['articles'][article],params['articles'][article]['uri'])

def buildTags():
	return 0

def buildTopics():
	return 0

def buildPages():
	return 0

def generateMedia():
	return 0

def generateAssets():
	os.makedirs('tmp/build/assets/css/',0o777,1)
	shutil.copy('assets/css/style.css','tmp/build/assets/css/style.css')
	return 0

def generateXML():
	return 0