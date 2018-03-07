import os
# from bsddb3 import db
# database = db.DB()
# database.set_flags(db.DB_DUP)

# delete the existing idx files to avoid open database flags error
os.system('rm -f *.idx')

# ----------------- for intermediate files debug ----------------- 
# os.system('sort -u terms.txt -o terms_sorted.txt')
# os.system('perl break.pl < terms_sorted.txt > terms_perl.txt')
# os.system('sort -u dates.txt -o dates_sorted.txt')
# os.system('perl break.pl < dates_sorted.txt > dates_perl.txt')
# os.system('sort -u tweets.txt -o tweets_sorted.txt')
# os.system('perl break.pl < tweets_sorted.txt > tweets_perl.txt')
# ----------------- for intermediate files debug ----------------- 

os.system('sort -u terms.txt | perl break.pl | db_load -c duplicates=1 -T -t btree te.idx')
os.system('sort -u dates.txt | perl break.pl | db_load -c duplicates=1 -T -t btree da.idx')
os.system('sort -u tweets.txt | perl break.pl | db_load -c duplicates=1 -T -t hash tw.idx')
os.system('db_dump -p -f 1.txt te.idx')
os.system('db_dump -p -f 2.txt da.idx')
os.system('db_dump -p -f 3.txt tw.idx')