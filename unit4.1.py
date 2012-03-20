'''
Web Crawler
-Vaishak Salin
'''
from urllib import urlopen
from bs4 import BeautifulSoup

index = {}  #Index is of type dict
splitlist = [' ','"',"'",'.',',','!','-']
def get_next_target(page):
    start_link = page.find('<a')    #Find anchor tag
    if start_link == -1:
        return None,0
    else:
        href = page.find('href',start_link) #Find href
        start_quote = page.find('"',href) #Find start quote
        end_quote = page.find('"',start_quote+1)    #Find end quote
        url = page[start_quote+1:end_quote] #Slice between quotes to get url
        return url,end_quote

def get_all_links(crawl_link): 
    try:
        f = urlopen(crawl_link) #The html code of the link is parsed and stored in page
        page = f.read()
        f.close()
    except:
        page = ""   #Incase of error it returns "" (empty)
    links = []
    content = page
    while True:
        url,end = get_next_target(page) #url and end are found
        if url:
            links.append(url)   
            page = page[end:]   #Value of page is updated to after end
        else:
            return links,content

def add_to_index(index,keyword,url):
    if keyword in index:    #Check if keyword is already in index
        index[keyword].append(url)
    else:
        index.setdefault(keyword,[url]) #add new index
        
def split_string(source,splitlist):
    for i in xrange(0,len(splitlist)):
        source = source.replace(splitlist[i]," ") 
    result = source.split()
    return result

def add_page_to_index(index,url,content):
    soup = BeautifulSoup(content)   #Using BeautifulSoup html is parsed to get only text
    html_text = soup.get_text()
    words = split_string(html_text,splitlist) #Split the content into words
    for word in words:
        add_to_index(index,word,url) #Index each word with urls in which it occurs

def lookup(index,keyword):  #Returns list of urls corresponding to given keyword
    if keyword in index:
        return index[keyword]
    else:
        return []   #If keyword is not indexed it returns an empty list

def search(query):
    keywords = query.split() #Each query is split into keywords
    urls = []
    search_result = []
    for keyword in keywords:
        urls = lookup(index,keyword)    #URLs indexed for every keyword is looked up
        for url in urls:
            if url not in search_result:    #Each URL occurs in list just once
                search_result.append(url)
    return search_result
  
def crawl_web(seed):
    to_crawl = [seed]   #Frontier queue which stores links that are to be crawled
    crawled = []    #Repository queue which stores links that have been crawled
    while to_crawl:
        crawl_link = to_crawl.pop() #A link to be crawled is popped out from to_crawl
        links,content = get_all_links(crawl_link)   #crawl_link is crawled links are returned
        for i in links:
            if i not in crawled:    #Each link is crawled only once
                to_crawl.append(i)
        add_page_to_index(index,crawl_link,content)
        crawled.append(crawl_link)
    return index
            
print crawl_web("http://www.udacity.com/cs101x/index.html") 
print search('I am learning')