import requests
import pickle
import json
import re
import urllib2
from bs4 import BeautifulSoup
import signal
import time
import sys
# from stanfordcorenlp import StanfordCoreNLP

# nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-10-05')
 
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
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', str(element.encode('utf-8'))):
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
                result = requests.get(query)
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
                        html = urllib2.urlopen(doc['link']).read() #urllib.request.urlopen(link)
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
                    result1=process(result)

                    fp.write(json.dumps({'link':doc['link'],'doc':result1.encode('utf-8')}))
                    fp.write('\n')
                    fp1=open('./docs/doc'+str(crawled)+'.txt','w')
                    # fp1=open('./docs/doc'+str(crawled)+'.txt','w')
                    fp1.write('<doc id="'+str(crawled)+'"'+'url="'+doc['link']+'"'+'title="'+doc['title']+'">\n')
                    fp1.write(doc['link']+'\n')
                    fp1.write(result1.encode('utf-8'))
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

