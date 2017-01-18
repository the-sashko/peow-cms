#!/usr/bin/python3
import jsonos,os
print('Sending...')
serverParams=json.loads(open('config/ssh.json','r').read())
os.system("./tools/send.sh "+serverParams['host']+" "+serverParams['user']+" "+serverParams['remotepath'])