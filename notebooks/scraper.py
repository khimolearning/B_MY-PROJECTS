#CELL 1
#BUILD THE SCRAPPER USING BEAUTIFUL SOUP
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from IPython.display import display, Markdown
import requests


def summarize_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }  #to bypass security an dprevent an empty response, we pose as a human being
    response = requests.get(url, headers=headers)
    webcode = response.text
    soup = BeautifulSoup(webcode, "html.parser")
    # 1. Create a blank "Summary" string to hold our structured text
    summary = ""

    # 2. Add the Title to the summary
    title_box = soup.find("h1")                          #check for a title tag "h1"
    if title_box:                                        #if u find a title tag                                                      
        summary += f"# {title_box.text}\n\n"             #do not print yet, add it to our container called "summary" (We add "#" for Markdown heading style and "\n\n" for space)
    else:
        summary += "# (No Title Found)\n\n"

    # 3. Add the Paragraphs to the Summary
    p_tags = soup.find_all("p")                          # find the paragraph tags "p". note; it puts it in a list at default.
    for p in p_tags:                                     # we have to take the orange one after the other from the basket to be able to peel the orange
        summary += f"{p.text}\n\n"                       # give me each paragraph but remove the tags give the texts ie, ".text"
    
    display(Markdown(summary))
    return summary                    # THE FINALE: Display the 'summary' we built, NOT the 'soup.text'




def get_links(url):
    # 1. Pose as a human to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # 2. Get the HTML code from the site
    response = requests.get(url, headers=headers)
    webcode = response.text
    
    # 3. Hand the code to the Chef
    soup = BeautifulSoup(webcode, "html.parser")
    
    link_data = [] 
    a_tags = soup.find_all("a")
    
    for a in a_tags:
        # Peel the name and the destination
        name = a.get_text().strip()
        url_destination = a.get('href')
        
        if url_destination:
            # Check if it's a real web address (http) and not just a page jump (#)
            if url_destination.startswith("http"):
                display_name = name if name else "(No Text Link)"
                link_data.append(f"NAME: {display_name} | URL: {url_destination}")
                
    return link_data



def summarize_dynamic_site(url):  # no more 'async'

    with sync_playwright() as p:                                          
        browser = p.chromium.launch(headless=True)      # launch the robot
        page = browser.new_page()                        # the robot opens a new page
        
        page.goto(url)                                   # the robot goes to the site
        page.wait_for_load_state("networkidle")          # wait till page loads completely
        page.wait_for_timeout(3000)
        full_html = page.content()                       # grab the page contents
        
        browser.close()                                  # shut down to preserve RAM

    soup = BeautifulSoup(full_html, "html.parser") 
    summary = ""
    title = soup.find("h1")
    if title:
        summary += f"TITLE: {title.text}\n\n"
    else:
        summary += "this text has got no heading\n\n"
    
    p_tags = soup.find_all("p")
    for p in p_tags:
        summary += f"{p.text}\n\n"

    return summary


#BUILD THE SCRAPPER TO SCRAPE LINKS

def get_links2(url):  # no more 'async'
    with sync_playwright() as p:                                          
        browser = p.chromium.launch(headless=True)      # launch the robot
        page = browser.new_page()                        # the robot opens a new page
        page.goto(url)                                   # the robot goes to the site
        page.wait_for_load_state("networkidle")          # wait till page loads completely
        full_html = page.content()                       # grab the page contents        
        browser.close()                                  # shut down to preserve RAM

    soup = BeautifulSoup(full_html, "html.parser") 
    link_data = "" 
    a_tags = soup.find_all("a")
    for a in a_tags:
        name = a.text.strip()
        url_destination = a.get('href')
        if url_destination:
            link_data += f"NAME: {name} | URL: {url_destination}\n\n"
    return link_data