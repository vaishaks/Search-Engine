'''
Web Crawler
-Vaishak Salin
'''
from urllib import urlopen
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None,0
    else:
        start_quote = page.find('"',start_link)
        end_quote = page.find('"',start_quote+1)
        url = page[start_quote+1:end_quote] 
        return url,end_quote

def get_all_links(crawl_link): 
    f = urlopen(crawl_link) #The html code of the link is parsed and stored in page
    page = f.read()
    f.close()
    links = []
    while True:
        url,end = get_next_target(page) #url and end are found
        if url:
            links.append(url)   
            page = page[end:]   #The html after the end is returned to function so the rest of the links are found
        else:
            return links
        
def crawl_web(seed):
    to_crawl = [seed]   #Frontier queue which stores all the links that are to be crawled
    crawled = []    #Repository queue which stores all the links that have been crawled
    while to_crawl:
        crawl_link = to_crawl.pop() #A link to be crawled is popped out from to_crawl
        links = get_all_links(crawl_link)   #crawl_link is crawled and all links are returned
        for i in links:
            if i not in crawled:    #Each link is crawled only once
                to_crawl.append(i)
        crawled.append(crawl_link)
    return crawled
            
    

print crawl_web("http://www.udacity.com/cs101x/index.html") 
       
