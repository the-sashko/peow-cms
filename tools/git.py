#!/usr/bin/python3
import json,os
print('Commit to git ...')
gitParams=json.loads(open('config/ssh.json','r').read())
os.system('git clone '+gitParams['repo']+' tmp/git')