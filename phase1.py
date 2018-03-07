import re
import os
fname=input("Enter the file name: ")
file=open(fname,'r')
fout1=open('terms.txt','w')
fout2=open('dates.txt','w')
fout3=open('tweets.txt','w')
for line in file:
    tid=re.findall(r'<id>(.+?)</id>',line)
    text=re.findall(r'<text>(.+?)</text>',line)
    tname=re.findall(r'<name>(.+?)</name>',line)
    tlocation=re.findall(r'<location>(.+?)</location>',line)
    tdate=re.findall(r'<created_at>(.+?)</created_at>',line)
    if len(text)!=0:
        r1=re.sub(r'&#\d+;','',text[0])
        rtext=re.split(r'[^0-9a-zA-Z_]',r1)
        for rt in rtext:
            if len(rt)>2:
                fout1.write("t-%s:"%rt.lower())
                fout1.write(tid[0]+"\n")

    if len(tname)!=0:	
        r2=re.sub(r'&#\d+;','',tname[0])
        rname=re.split(r'[^0-9a-zA-Z_]',r2)
        for rn in rname:
            if len(rn)>2:
                fout1.write("n-%s:"%rn.lower())
                fout1.write(tid[0]+"\n")

    if len(tlocation)!=0:
        r3=re.sub(r'&#\d+;','',tlocation[0])
        rlocation=re.split(r'[^0-9a-zA-Z_]',r3)
        for rl in rlocation:
            if len(rl)>2:
                fout1.write("l-%s:"%rl.lower())
                fout1.write(tid[0]+"\n")
    if len(tdate)!=0:
        fout2.write("%s:%s\n"%(tdate[0],tid[0]))
    if len(tid)!=0:
        fout3.write("%s:%s"%(tid[0],line))
file.close()
fout1.close()
fout2.close()
fout3.close()




























