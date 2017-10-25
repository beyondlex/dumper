import os

l = os.listdir('/home/lex/Documents/sqls')
l.sort()
for fname in l:
    i = fname.index('.')
    name = fname[:i]
    # print name
    f = "/home/lex/Documents/sqls/" + fname
    # sql = open(f).read()

