def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None,0
    else:
        start_quote = page.find('"',start_link)
        end_quote = page.find('"',start_quote+1)
        url = page[start_quote+1:end_quote] 
        return url,end_quote

def print_all_links(): 
    page = """<html><head></head><body><a href="http://www.x-art.com">X-Art</a><a href="http://www.google.com">asd</a></body></html>"""
    while True:
        url,end = get_next_target(page)
        if url:
            print url
            page = page[end:]
        else:
            break  

print_all_links() 
       
