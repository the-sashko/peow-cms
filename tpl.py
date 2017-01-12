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
		return res

	def makeVar(self,chunk,data):
		if(isinstance(data,dict)):
			if chunk.lower() in data:
				return str(data[chunk.lower()])
		return '{%'+chunk+'%}'

	def makeSubVar(self,chunk,index,data):
		if(isinstance(data,dict)):
			if chunk.lower() in data:
				chunkData=data[chunk.lower()]
				if(isinstance(chunkData,dict)):
					if index.lower() in chunkData:
						return str(chunkData[index.lower()])
		return '{%'+chunk+'|'+index+'%}'

	def calc(self,chunk):
		try:
			return str(eval(str(chunk)))
		except Exception as e:
			return '{{'+chunk+'}}'
	
	def condition(self,condition,trueVal,falseVal):
		return eval(str('str("'+trueVal+'") if '+condition+' else str("'+falseVal+'")'))

	def include(self,file):
		try:
			return str(open(file.lower()+'.html', 'r').read())
		except Exception as e:
			return '{!'+file+'!}'
		

testData={'name':'Sashko','x':'1','one':1,'two':2,'a':{'test','test2','test0'},'a2':{'aaa':{'name':'WAN'},'bbb':{'name':'too'}},'a3':{'one':'1','dwo':'2'},'foo':{'X','Y','Z'},'bar':{'A','B','C'}}
testTpl='{!TEMP!}'
test = Templator(testData,testTpl)
print(test.html)

#{!FILE!} | print(open('file.html').read())
#{%[VAR+1]%} | print(var+1)
#{%VAR|VAR2%} | print(var['var2'])
#{?%VAR%>%VAR2%?}...{?ELSE?}...{?END?} | print(...) if(4?4) else print(...)
#{@VAR:VAR2@}...{%VAR2%}...{@END@} | for var2 in var: ... print(var2) ...
#{@FOO:BAR@}...{%BAR%}...{@@FOO2:BAR2@}...{%BAR2%}...{@END@@}...{@END@} | for bar in foo: ... print(bar) ... for bar2 in foo2: ... print(bar2) ...
#{%VAR%} | print(var)
#<BR> | "\n"