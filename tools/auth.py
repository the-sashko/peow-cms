#!/usr/bin/python3
import json,os
print('Sending...')
serverParams=json.loads(open('config/ssh.json','r').read())
os.system('cat ~/.ssh/id_rsa.pub | ssh '+serverParams['user']+'@'+serverParams['host']+' "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"')