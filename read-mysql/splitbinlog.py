#!/usr/bin/python

import sys,re

queries = []
query = ''

while True:
    line = sys.stdin.readline()
    if not line:
        queries.append(query)
        break
    line = re.sub('^### ', '', line) 
    line = re.sub('\n', '', line) 
    line = re.sub('^ +', '', line) 
    line = re.sub(' +$', '', line) 
    if re.match('^INSERT', line) or re.match('^UPDATE', line) or re.match('^DELETE', line):
        if query != '':
            queries.append(query)
            query = ''
    query += line + ' '


for q in queries:
    print q + "\n"

