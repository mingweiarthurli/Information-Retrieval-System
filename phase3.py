import re
from bsddb3 import db

TE = 'te.idx'
DA = 'da.idx'
TW = 'tw.idx'

teDB = db.DB()
daDB = db.DB()
twDB = db.DB()
teDB.open(TE, None, db.DB_BTREE, db.DB_DIRTY_READ)
daDB.open(DA, None, db.DB_BTREE, db.DB_DIRTY_READ)
twDB.open(TW, None, db.DB_HASH, db.DB_DIRTY_READ)
teCurs = teDB.cursor()
daCurs = daDB.cursor()
twCurs = twDB.cursor()

def grammar():
    tids = []
    queries = input('Enter a searching query: ').lower()
    queries = queries.split(' ')
    queryNum = 0

    for query in queries:
        if ':' in query:
            query = query.split(':')
            if query[0] == 'text':
                termPrefix = 't-'
            elif query[0] == 'name':
                termPrefix = 'n-'
            elif query[0] == 'location':
                termPrefix = 'l-'
            elif query[0] == 'date':
                termPrefix = ''
            else:
                raise RuntimeError('invalid query')

            # this line can add some detection rule for invalid input of term
            if query[1][-1] == '%':
                if termPrefix == '':
                    raise RuntimeError('invalid query')
                else:
                    newTids = partialSearch(termPrefix, query[1][:-1])
            else:
                newTids = search(termPrefix, query[1])

        elif '>' in query:
            query = query.split('>')
            if query[0] != 'date':
                raise RuntimeError('invalid query')
            else:
                newTids = afterDate(query[1])

        elif '<' in query:
            query = query.split('<')
            if query[0] != 'date':
                raise RuntimeError('invalid query')
            else:
                newTids = beforeDate(query[1])

        elif query[-1] == '%': # this can be a more specific rule to avoid % is in the term rather than at the end
            textTids = partialSearch('t-', query[:-1])
            nameTids = partialSearch('n-', query[:-1])
            locationTids = partialSearch('l-', query[:-1])
            newTids = list(set(textTids).union(set(nameTids).union(locationTids)))

        else:
            textTids = search('t-', query)
            nameTids = search('n-', query)
            locationTids = search('l-', query)
            newTids = list(set(textTids).union(set(nameTids).union(locationTids)))

        # print(newTids)

        # if tids == []: This line is commented b/c it will cause bug when there are multiple queries and one of them is no result. When one query is no result, tids should be empty, but tids will be reset to newTids due to this line.
        if queryNum == 0:
            tids = newTids
        else:
            tids = list(set(tids).intersection(newTids))

        queryNum += 1

    return tids

def search(termPrefix, term):
    if termPrefix == '':
        curs = daCurs
    else:
        curs = teCurs

    key = termPrefix + term
    key = key.encode()
    results = []

    result = curs.get(key, db.DB_SET)
    while result != None: # curs.get(key, db.DB_NEXT_DUP) will return None if it reaches end
        # print(result)
        results.append(result[1])
        result = curs.get(key, db.DB_NEXT_DUP)

    return results

def partialSearch(termPrefix, term):
    key = termPrefix + term
    key = key.encode()
    results = []

    result = teCurs.get(key, db.DB_SET_RANGE)
    while result != None: # if there is no result, Nonetype cannot be compared with bytes
        if result[0].startswith(key):
            # print(result)
            results.append(result[1])
        else:
            break
        result = teCurs.get(key, db.DB_NEXT)

    return results

def afterDate(date):
    date = date.encode()
    results = []

    result = daCurs.get(date, db.DB_SET_RANGE)
    while result != None: # when the date goes through to the end, it will return None
        if result[0] != date: # we just want to include result after the given date
            # print(result)
            results.append(result[1])
        result = daCurs.get(date, db.DB_NEXT)

    return results

def beforeDate(date):
    date = date.encode()
    results = []

    result = daCurs.get(date, db.DB_SET_RANGE)
    result = daCurs.get(date, db.DB_PREV) # move the cursor to previous one
    while result != None: # when the date goes through to the end, it will return None
        # print(result)
        results.append(result[1])
        result = daCurs.get(date, db.DB_PREV) # since it goes through the databse reversely, the result will be from latest date to earliest date

    return results

def searchTweets(tids):
    for tid in tids:
        result = twCurs.get(tid, db.DB_SET)
        output(result[1])

def output(line):
    line = line.decode()
    # print('debug: ' + line)

    tid = re.findall(r'<id>(.+?)</id>', line)
    text = re.findall(r'<text>(.+?)</text>', line)
    tname = re.findall(r'<name>(.+?)</name>', line)
    tlocation = re.findall(r'<location>(.+?)</location>', line)
    tdate = re.findall(r'<created_at>(.+?)</created_at>', line)
    retweet = re.findall(r'<retweet_count>(.+?)</retweet_count>', line)
    description = re.findall(r'<description>(.+?)</description>', line)
    url = re.findall(r'<url>(.+?)</url>', line)
    print("tid: %s \nname: %s \nlocation: %s \ndate: %s \nretweet: %s \ndescription: %s \nurl: %s \ntext: %s" % (''.join(tid), ''.join(tname), ''.join(tlocation), ''.join(tdate),''.join(retweet),''.join(description),''.join(url), ''.join(text)))
    print('\n')

def main():
    invalidInput = True
    while invalidInput:
        try:
            tids = grammar()
            invalidInput = False
        except RuntimeError:
            print('invalid query')

    if tids == []:
        print('No result matches.')
    else:
        searchTweets(tids)

    teCurs.close()
    daCurs.close()
    twCurs.close()
    teDB.close()
    daDB.close()
    twDB.close()

main()
