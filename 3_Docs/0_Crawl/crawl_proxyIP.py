import requests
import pickle
import json
import re
import urllib2
from bs4 import BeautifulSoup
import signal
import time
import sys
import requesocks
import unicodedata

def test_request(arg=None):
    """Your http request."""
    time.sleep(2)
    return arg

class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

def visible(element):
    '''crawl visible'''
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def visible1(element):
    '''delete '''
    if re.match('\[.*\]', str(element.encode('utf-8'))):
            return False
    return True


def process(result):
    result1=''
    for elem in result:
        if elem.count(' ') <= 1:
            continue
        elem=elem.strip('\n')
        elem=elem.strip('\t')
        elem=elem.strip('\r')
        result1+=' '+elem
    return result1

headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
}

proxies = {
    'http': 'http://127.0.0.1:1087',
    'https': 'https://127.0.0.1:1087'}

def get_top10_GOOGLE(q):
    fp=open('./docs/link_wise_docs_'+q+'.json','w')
    links=[]
    line_count=0
    docs=[]
    start=1
    print "\n\nCrawling for ---> ",q
    crawled=0
    # qflag=0
    while crawled<10 and start<=11:
        qflag=0
        query='https://www.googleapis.com/customsearch/v1?key=AIzaSyBVB31PBqr7OBjunIjq8iPNb5L75pzTxzg&cx=000764406663250367259:rtvytnbpauk&q='+q+'&start='+str(start)
        try:
            with Timeout(40):
                headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'}
                result = requests.get(query, proxies=proxies, headers=headers)
                # result = requests.get(query)
                r=result.json()
                qflag=1
        except Timeout.Timeout:
            print "\n\nTimeout Google\n\n"
        except:
            print "\n\nCould not crawl google... ",start,q
        #print "done link"
        ct=0
        flag=0
        if qflag==1 and 'items' in r and r['items'][0]['kind']!='':
            for doc in r['items']:
                #print "link  ",start+ct, doc['link']
                flag=0
                try:
                    with Timeout(20):
                        #html = urllib2.urlopen(doc['link']).read() #urllib.request.urlopen(link)
                        opener = urllib2.build_opener(urllib2.ProxyHandler(proxies))
                        urllib2.install_opener(opener)
                        req = urllib2.Request(doc['link'], headers=headers)
                        html = urllib2.urlopen(req)
                        flag=1
                        
                except Timeout.Timeout:
                    flag=0
                    #print "\n\nTimeout"
                except:
                    flag=0
                    #print "\n\nCould not crawl ... ",start+ct,doc['link']
                if flag==1:
                    links.append(doc['link'])
                    crawled+=1
                    soup = BeautifulSoup(html,"lxml")
                    data = soup.findAll(text=True)
                    result = list(filter(visible, data))
                    result = list(filter(visible1, result))
                    # result = ''.join(map(delReturn, result)) # 
                    # result = result.strip() # 
                    # result = re.sub('\n{2,}', '\n\n', result) # 
                    result = process(result)
                    result = unicodedata.normalize(u'NFKD', result).encode('ascii', 'ignore').decode('utf8')
                    #result = re.sub('\n', '', result) # 
                    result = re.sub("\s", ' ', result)
                    result = re.sub(r'\'','', result)
                    fp.write(json.dumps({'link':doc['link'],'doc':result.encode('utf-8')}))
                    fp.write('\n')
                    fp1=open('./docs/doc'+str(crawled)+'.txt','w')
                    # fp1=open('./docs/doc'+str(crawled)+'.txt','w')
                    fp1.write('<doc id="'+str(crawled)+'"'+' url="'+doc['link']+'"'+' title="'+doc['title']+'">\n')
                    fp1.write(doc['title']+'\n\n')
                    fp1.write(result.encode('utf-8'))
                    fp1.write('\n\n\n\n\n</doc>')
                    fp1.close()
                    if len(docs)<10:
                        docs.append('./docs/doc'+str(crawled)+'.txt')
                #print "Done writing"
                ct+=1
        start+=10
        #print "Start ",start,crawled
    pickle.dump(links,open('./links/google_search_links_'+q,'w'))
    fp.close()
    return docs

def main(argv):
    print 'Arguments -> ',argv
    if len(argv)==2: #Only question is given
        question=argv[1]
        ### Crawling top 10 documents from Google 
        print "\n\nNo document provided...Crawling top 10 docs from Google..."
        docs=get_top10_GOOGLE(question)
        print "\n\nCrawling documents done...",len(docs),docs
    else:
        if len(argv)>=3 and len(argv)<=12: #Question is given with K documents, 10>=K>=1, no need to crawl
            question=argv[1]
            docs=[]
            for i in range(2,len(argv)):
                docs.append(argv[i])
            print "\n\n", len(argv)
            print "\n\nDocuments provided.. No need of crawling..."
        else:
            print "\n\nWrong number of arguments... Exiting ... \n"
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv)