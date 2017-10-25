import os

fo = open('.env', 'r')

map = {}
for line in fo.readlines():
    line = line.strip()
    if not line:
        continue
    if line[0] == '#':
        continue
    m = line.split('=')
    k = m[0]
    v = m[1]
    map[k] = v

config = map



