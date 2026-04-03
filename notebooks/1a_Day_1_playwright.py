#CELL 1
#BUILD THE SCRAPPER
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from IPython.display import display, Markdown

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

#CELL 2
#CALL THE API
from openai import OpenAI
client = OpenAI()

url = "https://khimoai.my.canva.site"
to_be_translated = summarize_dynamic_site(url)  # no more 'await'

my_system_prompt = "you are a smart virtual assistant who is perfect at summarizing a web page."
my_user_prompt = f"you will translate the content of this webpage {to_be_translated} into pidgin english"

my_messages = [
    {"role": "system", "content": my_system_prompt},
    {"role": "user", "content": my_user_prompt}
]

response = client.chat.completions.create(model="gpt-4o", messages=my_messages)
result = response.choices[0].message.content

print(result)