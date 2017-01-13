#!/usr/bin/python3
import re,sys

class Templator():
	data={}
	html='';

	def __init__(self,data,html):
		self.html=html
		self.data=data
		try:
			self.html=self.main(self.html,self.data)
		except Exception as e:
			print(e)
			sys.exit()
		
	def main(self,template,vars):
		template = re.sub(r'{!(.*?)!}',
			lambda data: self.include(data.group(1)),
			template,flags=re.U)
		template=re.sub('\r?\n', '<BR>', template)
		template = re.sub(r'{@(.*?):(.*?)@}(.*?){@END@}',
			lambda data: self.iterate(data.group(3),vars[data.group(1).lower()],data.group(2)),
			template,flags=re.M|re.U)
		template = re.sub(r'{@(.*?):(.*?)@}(.*?){@END@}',
			lambda data: self.iterate(data.group(3),vars[data.group(1).lower()],data.group(2)),
			template,flags=re.M|re.U)
		template = re.sub(r'{%(.*?)\|(.*?)%}',
			lambda data: self.makeSubVar(data.group(1),data.group(2),vars),
			template,flags=re.U)
		template = re.sub(r'{%(.*?)%}',
			lambda data: self.makeVar(data.group(1),vars),
			template,flags=re.U)
		template = re.sub(r'{{(.*?)}}',
			lambda data: self.calc(data.group(1)),
			template,flags=re.U)
		template = re.sub(r'{\?(.*?)(\>|\<|\=\=|\=\<|\=\>|\<\=|\>\=|\!\=)(.*?)\?}(.*?){\?ELSE\?}(.*){\?END\?}',
			lambda data: self.condition(str(data.group(1))+str(data.group(2))+str(data.group(3)),data.group(4),data.group(5)),
			template,flags=re.U)
		template=re.sub('<BR>', "\r\n", template)
		return template

	def iterate(self,template,vars,current):
		res=''
		for val in vars:
			res=res+template.replace('{%'+current+'%}',val)
			res=res.replace('{@@','{@');
			res=res.replace('@@}','@}');
			if(isinstance(vars,dict)):
				if(isinstance(vars[val],dict)):
					res=res.replace('{%'+current+'|','{%')
					res=self.main(res,vars[val])
		return self.main(res,self.data)

	def makeVar(self,chunk,data):
		if(isinstance(data,dict)):
			if chunk.lower() in data:
				return self.main(str(data[chunk.lower()]),self.data)
		return '{%'+chunk+'%}'

	def makeSubVar(self,chunk,index,data):
		if(isinstance(data,dict)):
			if chunk.lower() in data:
				chunkData=data[chunk.lower()]
				if(isinstance(chunkData,dict)):
					if index.lower() in chunkData:
						return self.main(str(chunkData[index.lower()]),self.data)
		return '{%'+chunk+'|'+index+'%}'

	def calc(self,chunk):
		try:
			return self.main(str(eval(str(chunk))),self.data)
		except Exception as e:
			return '{{'+chunk+'}}'
	
	def condition(self,condition,trueVal,falseVal):
		return self.main(str(eval(str('str("'+trueVal+'") if '+condition+' else str("'+falseVal+'")'))),self.data)

	def include(self,file):
		try:
			return self.main(str(open('html/layout/'+file.lower()+'.html', 'r').read()),self.data)
		except Exception as file:
			file=str(file)
			return '{!'+file+'!}'