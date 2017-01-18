#!/usr/bin/python3
from app import main
import sys
try:
  main.init()
except Exception as e:
  print('ERROR!')
  print(e)
sys.exit()
